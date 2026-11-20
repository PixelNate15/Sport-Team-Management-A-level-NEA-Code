"""
Prototype 5 database testing.

Run this file directly. It will:
  1. Remove any left-over test data from a previous (crashed) run
  2. Insert the test data it needs (everything is prefixed with TSTSQL)
  3. Run every test and print the results in the same format as testing_SQL.py
  4. Remove ALL the test data again (even if a test crashes), then prove it is gone
"""
from datetime import date, timedelta
from pprint import pprint

import SQL
from SQL import (
    connect_database,
    get_players_in_one_squad,
    get_last_ten_feedback_scores,
    get_club_id,
    get_all_players_for_squads_below_ranking,
    add_player_to_squad,
    get_squad_upcoming_fixtures,
    get_squad_results,
    remove_fixture,
    get_fixture_information,
    save_team_selection_players,
    insert_fixture,
    update_fixture,
    get_fixtures_without_results,
    get_result,
    get_players_for_fixture,
    get_matches_for_fixture,
    save_match_players,
    save_match,
)

TAG = "TSTSQL"                  # prefix on everything this file creates
SHOW_TEST_LABELS = True         # prints "Test: ..." above each test so screenshots are easy to match up
SHOW_SECTION_HEADINGS = True    # prints a heading before each function's tests

today = date.today()
ids = {}                        # stores the ids of all the test rows, eg ids["U_CAP"]


# ---------------------------------------------------------------- output helpers
def section(title):
    if SHOW_SECTION_HEADINGS:
        print("=" * 70)
        print(title)
        print("=" * 70)
        print()


def test(label, function, *parameters):
    if SHOW_TEST_LABELS:
        print("Test:", label)
    print("Function:", function.__name__)
    print("Parameters:", parameters)

    result = None
    try:
        result = function(*parameters)

        if isinstance(result, list):
            print(f"Returned (showing first {min(3, len(result))} of {len(result)}):")
            pprint(result[:3], sort_dicts=True)
        else:
            print("Data:", result)

    except Exception as err:
        print("Error:", err)

    print()
    return result


def check(label, sql, params=()):
    """Runs a read-only query so the effect of an insert/update/delete can be seen."""
    print("Check:", label)
    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        pprint(rows, sort_dicts=True)
    except Exception as err:
        print("Error:", err)
    print()


def test_with_cursor(label, function, *parameters):
    """For functions that need an open cursor (save_team_selection_players, save_match_players)."""
    if SHOW_TEST_LABELS:
        print("Test:", label)
    print("Function:", function.__name__)
    print("Parameters:", parameters)
    connection = connect_database()
    cursor = connection.cursor()
    try:
        result = function(cursor, *parameters)
        connection.commit()
        print("Data:", result)
    except Exception as err:
        connection.rollback()
        print("Error:", err)
    cursor.close()
    connection.close()
    print()


def skipped(function_name, labels):
    section(function_name)
    for label in labels:
        if SHOW_TEST_LABELS:
            print("Test:", label)
        print("Function:", function_name)
        print("Skipped: this function is not in SQL.py yet")
        print()


# ---------------------------------------------------------------- db helpers
def setup_rows(work):
    """Opens a connection, runs work(cursor), commits and returns whatever work returns."""
    connection = connect_database()
    cursor = connection.cursor()
    try:
        result = work(cursor)
        connection.commit()
        return result
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def _conditions(conditions):
    clauses, params = [], []
    for column, id_list in conditions:
        if id_list:
            clauses.append(f"{column} IN ({', '.join(['%s'] * len(id_list))})")
            params.extend(id_list)
    return clauses, params


def select_in(cursor, table, id_column, *conditions):
    clauses, params = _conditions(conditions)
    if not clauses:
        return []
    cursor.execute(f"SELECT {id_column} FROM {table} WHERE {' OR '.join(clauses)}", params)
    return [row[0] for row in cursor.fetchall()]


def delete_in(cursor, table, *conditions):
    clauses, params = _conditions(conditions)
    if clauses:
        cursor.execute(f"DELETE FROM {table} WHERE {' OR '.join(clauses)}", params)


def cleanup(cursor):
    """Removes every row that belongs to the test data, in foreign key order."""
    cursor.execute("SELECT user_id FROM `user` WHERE username LIKE %s", (f"{TAG}%",))
    users = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT club_id FROM club WHERE club_name = %s", (f"{TAG} Club",))
    clubs = [row[0] for row in cursor.fetchall()]

    squads = select_in(cursor, "squad", "squad_id", ("club_id", clubs))
    fixtures = select_in(cursor, "fixture", "fixture_id", ("squad_id", squads), ("created_by_id", users))
    team_selections = select_in(cursor, "team_selection", "team_selection_id", ("fixture_id", fixtures))
    matches = select_in(cursor, "`match`", "match_id", ("fixture_id", fixtures))

    delete_in(cursor, "partner_feedback", ("match_id", matches), ("reviewer_id", users), ("reviewed_id", users))
    delete_in(cursor, "match_players", ("match_id", matches), ("user_id", users), ("partner_user_id", users))
    delete_in(cursor, "`match`", ("match_id", matches))
    delete_in(cursor, "team_selection_players", ("team_selection_id", team_selections), ("user_id", users))
    delete_in(cursor, "team_selection", ("team_selection_id", team_selections))
    delete_in(cursor, "availability", ("fixture_id", fixtures), ("user_id", users))
    delete_in(cursor, "fixture", ("fixture_id", fixtures))
    delete_in(cursor, "injury", ("user_id", users))
    delete_in(cursor, "settings", ("user_id", users))
    delete_in(cursor, "squad_players", ("squad_id", squads), ("user_id", users))
    delete_in(cursor, "squad", ("squad_id", squads))
    delete_in(cursor, "`user`", ("user_id", users))
    delete_in(cursor, "club", ("club_id", clubs))
    cursor.execute("DELETE FROM division WHERE division_name = %s", (f"{TAG} Division",))
    cursor.execute("DELETE FROM season WHERE season_name = %s", (f"{TAG} Season",))


def team(keys):
    """Turns 4 user keys into the list of dictionaries the SQL functions need."""
    return [{"user_id": ids[key], "pair_number": 1 if i < 2 else 2, "selection_order": (i % 2) + 1}
            for i, key in enumerate(keys)]


def _add_fixture_row(cursor, opponent, days, squad_key, notes="Test notes", opp_position=5):
    cursor.execute("""
        INSERT INTO fixture
        (created_by_id, opponent_name, date, start_time, location, is_home, division,
         opponent_league_position, notes, squad_id, season_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (ids["U_CAP"], opponent, today + timedelta(days=days), "14:00:00", "Test Court", 1,
          ids["division"], opp_position, notes, ids[f"S_{squad_key}"], ids["season"]))
    return cursor.lastrowid


def _add_team_rows(cursor, fixture_id, keys):
    cursor.execute("INSERT INTO team_selection (fixture_id, date) VALUES (%s, %s)", (fixture_id, today))
    team_selection_id = cursor.lastrowid
    for player in team(keys):
        cursor.execute("""
            INSERT INTO team_selection_players (team_selection_id, user_id, pair_number, selection_order)
            VALUES (%s, %s, %s, %s)
        """, (team_selection_id, player["user_id"], player["pair_number"], player["selection_order"]))


def _add_match_rows(cursor, fixture_id, pair, days, did_win, sets, games, set_scores, player_1, player_2,
                    with_players=True):
    cursor.execute("""
        INSERT INTO `match`
        (fixture_id, pair_number, opponent_pair_number, date, did_win, sets_won, sets_lost, games_won, games_lost,
         set_1_won, set_1_lost, set_2_won, set_2_lost, champ_tie)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (fixture_id, pair, pair, today + timedelta(days=days), did_win, sets[0], sets[1], games[0], games[1],
          set_scores[0], set_scores[1], set_scores[2], set_scores[3], None))
    match_id = cursor.lastrowid
    for user, partner in (((player_1, player_2), (player_2, player_1)) if with_players else ()):
        cursor.execute("""
            INSERT INTO match_players (match_id, user_id, partner_user_id, partner_form_at_match)
            VALUES (%s, %s, %s, %s)
        """, (match_id, ids[user], ids[partner], None))
    return match_id


def _add_feedback_rows(cursor, match_id, reviewer, reviewed, overall_scores):
    for index, overall in enumerate(overall_scores):
        cursor.execute("""
            INSERT INTO partner_feedback
            (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (match_id, ids[reviewer], ids[reviewed], overall, max(overall - 1, 0), min(overall + 1, 10),
              f"Test feedback {index + 1}", today - timedelta(days=(len(overall_scores) - index))))


def new_fixture(days=30, squad="A", team_keys=None, availability=False, opp="Test Opponent",
                opp_position=5, notes="Test notes"):
    """Creates a one-off fixture (and optionally a team selection/availability) for a single test."""
    def work(cursor):
        fixture_id = _add_fixture_row(cursor, opp, days, squad, notes, opp_position)
        if team_keys:
            _add_team_rows(cursor, fixture_id, team_keys)
        if availability:
            cursor.execute("""
                INSERT INTO availability (fixture_id, user_id, is_available, reason, date_submitted)
                VALUES (%s, %s, %s, %s, %s)
            """, (fixture_id, ids["U_A1"], 0, "Test reason", today))
        return fixture_id
    return setup_rows(work)


def new_match(fixture_id, player_1="U_CAP", player_2="U_A1", with_players=True):
    """Creates a match (and optionally its two players) on a fixture. Returns the match_id."""
    return setup_rows(lambda cursor: _add_match_rows(cursor, fixture_id, 1, -5, 1, (2, 0), (12, 6),
                                                    (6, 3, 6, 3), player_1, player_2, with_players))


def match_dict(player_1, player_2, form_1=0.75, form_2=0.5, **changes):
    match = {
        "pair_number": 1, "opponent_pair_number": 1,
        "sets_won": 2, "sets_lost": 0, "games_won": 12, "games_lost": 5,
        "set_1_won": 6, "set_1_lost": 2, "set_2_won": 6, "set_2_lost": 3, "champ_tie": None,
        "player_1": ids[player_1], "player_2": ids[player_2], "form_1": form_1, "form_2": form_2,
    }
    match.update(changes)
    return match


MATCH_PLAYERS_CHECK = """
    SELECT mp.user_id, mp.partner_user_id, mp.partner_form_at_match
    FROM match_players mp
    WHERE mp.match_id = %s
    ORDER BY mp.user_id
"""

MATCH_FIXTURE_CHECK = """
    SELECT m.match_id, m.pair_number, m.did_win, m.sets_won, m.sets_lost, m.games_won, m.games_lost,
           (SELECT COUNT(*) FROM match_players mp WHERE mp.match_id = m.match_id) AS player_rows
    FROM `match` m
    WHERE m.fixture_id = %s
    ORDER BY m.match_id
"""


# ---------------------------------------------------------------- test data
def setup():
    def work(cursor):
        cleanup(cursor)

        cursor.execute("INSERT INTO club (club_name) VALUES (%s)", (f"{TAG} Club",))
        ids["club"] = cursor.lastrowid

        cursor.execute("INSERT INTO division (division_name, team_count) VALUES (%s, %s)", (f"{TAG} Division", 10))
        ids["division"] = cursor.lastrowid

        #Uses the real current season if there is one, so there is only ever one current season
        cursor.execute("SELECT season_id FROM season WHERE is_current = 1 LIMIT 1")
        row = cursor.fetchone()
        if row:
            ids["season"] = row[0]
        else:
            cursor.execute("INSERT INTO season (season_name, is_current) VALUES (%s, 1)", (f"{TAG} Season",))
            ids["season"] = cursor.lastrowid

        #Squads: A is the highest, D is the lowest
        for key, ranking in (("A", 1), ("B", 2), ("C", 3), ("D", 4)):
            cursor.execute("""
                INSERT INTO squad (squad_name, squad_ranking, club_id, division_id)
                VALUES (%s, %s, %s, %s)
            """, (f"{TAG} Squad {key}", ranking, ids["club"], ids["division"]))
            ids[f"S_{key}"] = cursor.lastrowid

        #Users: (key, squad or None, is_captain, has a club)
        users = [
            ("U_CAP", "A", True, True), ("U_A1", "A", False, True), ("U_A2", "A", False, True),
            ("U_A3", "A", False, True), ("U_B1", "B", False, True), ("U_B2", "B", False, True),
            ("U_C1", "C", False, True), ("U_C2", "C", False, True), ("U_D1", "D", False, True),
            ("U_NOSQUAD", None, False, True),     #in a club but not in any squad
            ("U_NOCLUB", None, False, False),     #club_id is NULL
        ]
        for key, squad, is_captain, has_club in users:
            cursor.execute("""
                INSERT INTO `user`
                (first_name, surname, username, password_hash, date_of_birth, is_captain, email, is_active, club_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (key.replace("U_", "").title(), "Tester", f"{TAG}_{key}", "not_a_real_hash", date(2000, 1, 1),
                  is_captain, f"{key}@test.com", True, ids["club"] if has_club else None))
            ids[key] = cursor.lastrowid
            if squad:
                cursor.execute("INSERT INTO squad_players (squad_id, user_id) VALUES (%s, %s)",
                               (ids[f"S_{squad}"], ids[key]))

        #Fixtures
        ids["F_A_FUT1"] = _add_fixture_row(cursor, "Test Opp A Future 1", 10, "A")
        _add_team_rows(cursor, ids["F_A_FUT1"], ["U_CAP", "U_A1", "U_A2", "U_A3"])
        ids["F_A_FUT2"] = _add_fixture_row(cursor, "Test Opp A Future 2", 20, "A")
        ids["F_A_PAST_RES"] = _add_fixture_row(cursor, "Test Opp A Past Result", -30, "A")
        ids["F_A_PAST_NORES"] = _add_fixture_row(cursor, "Test Opp A Past No Result", -20, "A")
        ids["F_B_FUT"] = _add_fixture_row(cursor, "Test Opp B Future", 15, "B")
        ids["F_C_PAST"] = _add_fixture_row(cursor, "Test Opp C Past Result", -25, "C")
        ids["F_D_PAST"] = _add_fixture_row(cursor, "Test Opp D Past No Result", -10, "D")

        #Matches (only the fixtures that should have a result)
        ids["M1"] = _add_match_rows(cursor, ids["F_A_PAST_RES"], 1, -30, 1, (2, 0), (12, 5), (6, 2, 6, 3), "U_CAP", "U_A1")
        ids["M2"] = _add_match_rows(cursor, ids["F_A_PAST_RES"], 2, -30, 0, (0, 2), (5, 12), (3, 6, 2, 6), "U_A2", "U_A3")
        _add_match_rows(cursor, ids["F_C_PAST"], 1, -25, 1, (2, 0), (12, 7), (6, 3, 6, 4), "U_C1", "U_C2")

        #Feedback: A1 has 12 (more than 10), A2 has 4 (fewer than 10), A3 has none
        _add_feedback_rows(cursor, ids["M1"], "U_CAP", "U_A1", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8])
        _add_feedback_rows(cursor, ids["M2"], "U_A3", "U_A2", [5, 6, 7, 8])

    setup_rows(work)


def teardown():
    setup_rows(cleanup)
    print("=" * 70)
    print("Test data removal")
    print("=" * 70)
    print()
    check("Any test rows left in the database (everything should be 0)", """
        SELECT
            (SELECT COUNT(*) FROM `user` WHERE username LIKE %s) AS users,
            (SELECT COUNT(*) FROM club WHERE club_name = %s) AS clubs,
            (SELECT COUNT(*) FROM squad WHERE squad_name LIKE %s) AS squads,
            (SELECT COUNT(*) FROM fixture WHERE opponent_name LIKE %s) AS fixtures,
            (SELECT COUNT(*) FROM division WHERE division_name = %s) AS divisions,
            (SELECT COUNT(*) FROM season WHERE season_name = %s) AS seasons
    """, (f"{TAG}%", f"{TAG} Club", f"{TAG}%", "Test Opp%", f"{TAG} Division", f"{TAG} Season"))


# ---------------------------------------------------------------- the tests
def run_tests():
    #-------------------------------------------------------------- Get Players in One Squad
    section("Get Players in One Squad")
    test("Squad with several players", get_players_in_one_squad, ids["U_CAP"])
    test("Squad with no players", get_players_in_one_squad, ids["U_NOSQUAD"])

    #-------------------------------------------------------------- Get Last 10 Feedback Scores
    section("Get Last 10 Feedback Scores")
    test("Player with more than 10 feedback scores", get_last_ten_feedback_scores, ids["U_A1"])
    test("Player with fewer than 10 feedback scores", get_last_ten_feedback_scores, ids["U_A2"])
    test("Player with no feedback scores", get_last_ten_feedback_scores, ids["U_A3"])

    #-------------------------------------------------------------- Get Club ID
    section("Get Club ID")
    test("Valid User ID", get_club_id, ids["U_CAP"])
    test("User with a null Club ID", get_club_id, ids["U_NOCLUB"])

    #-------------------------------------------------------------- Get All Players for Squads Below Ranking
    section("Get All Players for Squads Below Ranking")
    test("Captain of the highest squad", get_all_players_for_squads_below_ranking, ids["U_CAP"], ids["club"])
    test("Captain of the lowest squad", get_all_players_for_squads_below_ranking, ids["U_D1"], ids["club"])

    #-------------------------------------------------------------- Add Player to Squad
    section("Add Player to Squad")
    squad_check = """
        SELECT u.first_name, sq.squad_name, sq.squad_ranking
        FROM squad_players sp
        JOIN squad sq ON sq.squad_id = sp.squad_id
        JOIN `user` u ON u.user_id = sp.user_id
        WHERE sp.user_id = %s
    """
    check("Player's squad BEFORE (squad B)", squad_check, (ids["U_B1"],))
    test("Valid captain and player ID for a player in a lower squad", add_player_to_squad, ids["U_CAP"], ids["U_B1"])
    check("Player's squad AFTER (should now be squad A)", squad_check, (ids["U_B1"],))

    #-------------------------------------------------------------- Get Squad Upcoming Fixtures
    section("Get Squad Upcoming Fixtures")
    test("Squad has future fixtures", get_squad_upcoming_fixtures, ids["U_B2"])
    test("Squad only has previous fixtures", get_squad_upcoming_fixtures, ids["U_C1"])
    test("Squad has both previous and future fixtures", get_squad_upcoming_fixtures, ids["U_CAP"])

    #-------------------------------------------------------------- Get Squad Results
    section("Get Squad Results")
    test("Squad with results", get_squad_results, ids["U_CAP"])
    test("Squad with no results", get_squad_results, ids["U_B2"])
    test("Fixtures in the past with no corresponding result", get_squad_results, ids["U_D1"])

    #-------------------------------------------------------------- Remove Fixture
    section("Remove Fixture")
    dependents = """
        SELECT
            (SELECT COUNT(*) FROM fixture WHERE fixture_id = %s) AS fixture_rows,
            (SELECT COUNT(*) FROM team_selection WHERE fixture_id = %s) AS team_selection_rows,
            (SELECT COUNT(*) FROM team_selection_players tsp
                JOIN team_selection ts ON ts.team_selection_id = tsp.team_selection_id
                WHERE ts.fixture_id = %s) AS team_selection_players_rows,
            (SELECT COUNT(*) FROM availability WHERE fixture_id = %s) AS availability_rows
    """
    with_dependents = new_fixture(days=40, team_keys=["U_CAP", "U_A1", "U_A2", "U_A3"], availability=True)
    check("Rows BEFORE removal (fixture with team selection and availability)", dependents, (with_dependents,) * 4)
    test("Fixture with corresponding team selection and availability rows", remove_fixture, with_dependents)
    check("Rows AFTER removal (everything should be 0)", dependents, (with_dependents,) * 4)

    without_dependents = new_fixture(days=41)
    check("Rows BEFORE removal (fixture on its own)", dependents, (without_dependents,) * 4)
    test("Fixture without corresponding team selection and availability rows", remove_fixture, without_dependents)
    check("Rows AFTER removal (everything should be 0)", dependents, (without_dependents,) * 4)

    #-------------------------------------------------------------- Get Fixture Information
    section("Get Fixture Information")
    test("Valid fixture ID", get_fixture_information, ids["F_A_FUT1"])
    null_fixture = new_fixture(days=42, opp_position=None, notes=None)
    test("Fixture with Null league position and notes", get_fixture_information, null_fixture)

    #-------------------------------------------------------------- Save Team Selection
    section("Save Team Selection")
    with_previous = new_fixture(days=43, team_keys=["U_CAP", "U_A1", "U_A2", "U_A3"])
    without_previous = new_fixture(days=44)

    new_players = team(["U_A1", "U_B2", "U_C1", "U_C2"])
    test("Check: team BEFORE saving", get_players_for_fixture, with_previous)
    test_with_cursor("Valid data with a previous team selection", save_team_selection_players, with_previous, new_players)
    test("Check: team AFTER saving (old players should be gone)", get_players_for_fixture, with_previous)

    test("Check: team BEFORE saving", get_players_for_fixture, without_previous)
    test_with_cursor("Valid data without a previous team selection", save_team_selection_players, without_previous, new_players)
    test("Check: team AFTER saving (new team selection created)", get_players_for_fixture, without_previous)

    #-------------------------------------------------------------- Insert Fixture
    section("Insert Fixture")
    captain = ids["U_CAP"]
    new_id = test("Valid data with 4 players", insert_fixture, captain, "Test Opp Inserted 1",
                  today + timedelta(days=50), "14:00", "Test Court", True, 4, "Inserted with a team",
                  team(["U_CAP", "U_A1", "U_A2", "U_A3"]))
    if new_id:
        test("Check: fixture that was inserted", get_fixture_information, new_id)
        test("Check: players that were inserted", get_players_for_fixture, new_id)

    new_id = test("Valid data with 0 players", insert_fixture, captain, "Test Opp Inserted 2",
                  today + timedelta(days=51), "15:00", "Test Court", False, 6, None, None)
    if new_id:
        test("Check: fixture that was inserted", get_fixture_information, new_id)
        test("Check: players that were inserted (should be empty)", get_players_for_fixture, new_id)

    test("Invalid Data", insert_fixture, captain, None, today + timedelta(days=52), "16:00",
         "Test Court", True, 3, None, None)
    check("Fixtures with the invalid opponent name (should be none)", """
        SELECT COUNT(*) AS fixtures_inserted
        FROM fixture
        WHERE created_by_id = %s AND date = %s
    """, (captain, today + timedelta(days=52)))

    #-------------------------------------------------------------- Update Fixture
    section("Update Fixture")
    update_1 = new_fixture(days=60, team_keys=["U_CAP", "U_A1", "U_A2", "U_A3"], opp="Test Opp Before Update")
    test("Check: fixture BEFORE update", get_fixture_information, update_1)
    test("Valid new data", update_fixture, update_1, "Test Opp After Update", today + timedelta(days=61),
         "16:30", "New Court", False, 3, "Updated notes")
    test("Check: fixture AFTER update", get_fixture_information, update_1)

    update_2 = new_fixture(days=62, team_keys=["U_CAP", "U_A1", "U_A2", "U_A3"])
    test("Check: team BEFORE update", get_players_for_fixture, update_2)
    test("Valid details with a changed team", update_fixture, update_2, "Test Opp Changed Team",
         today + timedelta(days=62), "14:00", "Test Court", True, 5, "Team changed",
         team(["U_A3", "U_A2", "U_B2", "U_C1"]))
    test("Check: team AFTER update (old players replaced)", get_players_for_fixture, update_2)

    #The fixture details are valid but one player does not exist, so the team part fails and everything must roll back
    update_3 = new_fixture(days=63, team_keys=["U_CAP", "U_A1", "U_A2", "U_A3"], opp="Test Opp Rollback")
    test("Check: fixture BEFORE failed update", get_fixture_information, update_3)
    test("Check: team BEFORE failed update", get_players_for_fixture, update_3)
    bad_team = [{"user_id": 999999999, "pair_number": 1, "selection_order": 1}]
    test("Invalid Data", update_fixture, update_3, "Test Opp SHOULD NOT SAVE", today + timedelta(days=64),
         "10:00", "Wrong Court", False, 9, "SHOULD NOT SAVE", bad_team)
    test("Check: fixture AFTER failed update (should be unchanged)", get_fixture_information, update_3)
    test("Check: team AFTER failed update (should be unchanged)", get_players_for_fixture, update_3)

    #-------------------------------------------------------------- Get Fixture Without Results
    section("Get Fixture Without Results")
    test("Squad with past fixtures with no corresponding match rows", get_fixtures_without_results, ids["U_D1"])
    test("Squads where all past fixtures have results", get_fixtures_without_results, ids["U_C1"])
    test("Squad with only future fixtures", get_fixtures_without_results, ids["U_B2"])

    #-------------------------------------------------------------- Get Result
    section("Get Result")
    test("Fixtures with corresponding match rows", get_result, ids["F_A_PAST_RES"])
    test("Fixtures with no match rows", get_result, ids["F_A_PAST_NORES"])

    #-------------------------------------------------------------- Get Matches for Fixture
    section("Get Matches for Fixture")
    test("Fixtures with saved matches", get_matches_for_fixture, ids["F_A_PAST_RES"])
    test("Fixtures with no saved matches", get_matches_for_fixture, ids["F_A_PAST_NORES"])

    #-------------------------------------------------------------- Save Match Players
    section("Save Match Players")
    match_fixture = new_fixture(days=-5)

    match_a = new_match(match_fixture, with_players=False)
    check("Players BEFORE saving (match has no players)", MATCH_PLAYERS_CHECK, (match_a,))
    test_with_cursor("Valid match ID with 2 different players", save_match_players, match_a,
                     match_dict("U_A2", "U_A3"))
    check("Players AFTER saving (2 rows)", MATCH_PLAYERS_CHECK, (match_a,))

    match_b = new_match(match_fixture, "U_CAP", "U_A1")
    check("Players BEFORE saving (CAP and A1)", MATCH_PLAYERS_CHECK, (match_b,))
    test_with_cursor("Existing match with 2 saved players, changed to 2 different players", save_match_players,
                     match_b, match_dict("U_A2", "U_A3", 0.6, 0.4))
    check("Players AFTER saving (should only be A2 and A3)", MATCH_PLAYERS_CHECK, (match_b,))

    match_c = new_match(match_fixture, "U_CAP", "U_A1")
    check("Players BEFORE saving", MATCH_PLAYERS_CHECK, (match_c,))
    test_with_cursor("Existing match with the same 2 players", save_match_players, match_c,
                     match_dict("U_CAP", "U_A1"))
    check("Players AFTER saving (still exactly 2 rows, no duplicates)", MATCH_PLAYERS_CHECK, (match_c,))

    #-------------------------------------------------------------- Save Match
    section("Save Match")
    save_fixture = new_fixture(days=-4)
    save_date = today + timedelta(days=-4)

    check("Matches BEFORE saving (none)", MATCH_FIXTURE_CHECK, (save_fixture,))
    test("Valid fixture ID, match details and is a new match", save_match, save_fixture, save_date,
         match_dict("U_CAP", "U_A1"), True)
    check("Matches AFTER saving (1 match with 2 player rows)", MATCH_FIXTURE_CHECK, (save_fixture,))

    existing_match = new_match(save_fixture, "U_CAP", "U_A1")
    edit = match_dict("U_A2", "U_A3", sets_won=0, sets_lost=2, games_won=4, games_lost=12,
                      set_1_won=2, set_1_lost=6, set_2_won=2, set_2_lost=6, match_id=existing_match)
    check("Match BEFORE editing", MATCH_FIXTURE_CHECK, (save_fixture,))
    check("Players BEFORE editing", MATCH_PLAYERS_CHECK, (existing_match,))
    test("Valid fixture ID, match details and is not a new match", save_match, save_fixture, save_date, edit, False)
    check("Match AFTER editing (now a loss, 0 - 2)", MATCH_FIXTURE_CHECK, (save_fixture,))
    check("Players AFTER editing (should be A2 and A3)", MATCH_PLAYERS_CHECK, (existing_match,))


if __name__ == "__main__":
    if connect_database() is None:
        raise SystemExit("Could not connect to the database, nothing was tested")

    setup()
    try:
        run_tests()
    finally:
        teardown()