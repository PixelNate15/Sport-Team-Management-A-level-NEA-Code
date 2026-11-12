import mysql.connector
from home_ip import getHomeIP
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

#Function to covert the timedelta into time
def format_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


#Function to connect to the database
def connect_database():
    try:
        #myIP = getHomeIP()
        username = "alevel_user"
        password = "b6ZMUxyMrEdPU1oSjJfLRFBvTOVJWH7h"
        # myIP = "localhost"
        # username = "root"
        # password = ""
        connection = mysql.connector.connect(
            host="90.217.20.215",
            user=username,
            password=password,
            database="alevel_app"
        )

        return connection

    except ConnectionError:
        print("ERROR: Could not connect to database")
        return None

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None


#Function to get the user_id of a user from the db from their username - requires username
def get_user_id(username: str) -> int:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT user_id
            FROM user
            WHERE username = %s
        """
        value = (username,)

        cursor.execute(sql, value)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return result[0]
        return None
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to add the information from the create account screen to the db, return the userID for easy transferring to the main screen
def insert_account_details(firstname: str, surname: str, date_of_birth: datetime, username: str, password_hash: str, email: str) -> int:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            INSERT into user
            (first_name, surname, username, password_hash, date_of_birth, is_captain, email, is_active)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (firstname, surname, username, password_hash, date_of_birth, False, email, True)

        cursor.execute(sql, values)
        connection.commit()

        new_user_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return new_user_id
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to check that a username is not already in the db - requires username
def check_for_duplicate_username(username: str) -> bool:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT user_id
            FROM user
            WHERE username = %s
        """
        value = (username,)

        cursor.execute(sql, value)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return True
        return False
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the password hash from the db for a certain username - requires username
def check_password_hash(username: str) -> str:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT password_hash
            FROM user
            WHERE username = %s
        """
        value = (username,)

        cursor.execute(sql, value)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return result[0]
        else:
            return None
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to check whether a user is a coach or a normal member - requires user_id
def check_is_captain(user_id: int) -> bool:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT is_captain
            FROM user
            WHERE user_id = %s
        """
        value = (user_id,)

        cursor.execute(sql, value)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is None:
            return False
        return bool(result[0])
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get all fixtures for a user for the team that they are involved in - requires user_id and an option variable of availability_filter
def get_fixtures(user_id: int, availability_filter: bool | None = None) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.start_time, f.location, f.is_home, f.notes, f.division,
            CASE WHEN tsp.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_selected
            FROM fixture f
            JOIN squad_players sp ON sp.squad_id = f.squad_id
            LEFT JOIN team_selection ts ON ts.fixture_id = f.fixture_id
            LEFT JOIN team_selection_players tsp ON tsp.team_selection_id = ts.team_selection_id AND tsp.user_id = %s
            WHERE sp.user_id = %s AND f.date >= CURDATE()
        """

        #Adds a filter so that only fixtures the user already stated their availability are retrieved
        if availability_filter == True:
            sql = sql + """
            AND EXISTS(
            SELECT 1
            FROM availability a
            WHERE a.fixture_id = f.fixture_id AND a.user_id = sp.user_id)
            """

        #Adds a filter so that only fixture the user have not stated their availability are retrieved
        if availability_filter == False:
                sql = sql + """
                AND NOT EXISTS(
                SELECT 1
                FROM availability a
                WHERE a.fixture_id = f.fixture_id AND a.user_id = sp.user_id)
                """

        #Orders the fixtures by date in ascending order
        sql = sql + "ORDER BY f.date ASC, f.start_time ASC"

        values = (user_id, user_id)

        cursor.execute(sql, values)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        fixtures = []
        for row in results:
            fixtures.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "start_time" : format_time(row[3]),
                "location" : row[4],
                "home_away" : ("Home" if row[5] else "Away"),
                "notes" : row[6],
                "division" : row[7],
                "is_selected" : bool(row[8])
            })

        return fixtures
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Functon to get the availiability of a fixture for a user which has already submitted their availability, requires user_id and fixture_id
def get_availability_details(user_id: int, fixture_id: int) -> dict:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT availability_id, is_available, reason
            FROM availability
            WHERE user_id = %s and fixture_id = %s
        """

        values = (user_id, fixture_id)

        cursor.execute(sql, values)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        details = {
            "availability_id": results[0],
            "is_available": results[1],
            "reason": results [2]
        }

        return details
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to insert the availability of a member for a fixture - requires fixture_id, user_id, is_available and an optional variable of reason
def insert_availability_details(fixture_id: int, user_id: int, is_available: bool, reason: str | None = None) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            INSERT into availability
            (fixture_id, user_id, is_available, reason, date_submitted)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (fixture_id, user_id, is_available, reason, date.today())

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to update the availability for a fixture - requires availability_id, is_available and an optional variable of reason
def update_availability_details(availability_id: int, is_available: bool, reason: str | None = None) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        if is_available == False:
            sql = """
                UPDATE availability
                SET is_available = %s, reason = %s
                WHERE availability_id = %s
            """
            values = (is_available, reason, availability_id)

        else:
            sql = """
                UPDATE availability
                SET is_available = %s, reason = NULL
                WHERE availability_id = %s
                """
            values = (is_available, availability_id)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the pair and players for a fixture - requires fixture_id
def get_players_for_fixture(fixture_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT tsp.user_id, tsp.pair_number, tsp.selection_order, u.first_name, u.surname
            FROM team_selection ts
            JOIN team_selection_players tsp ON tsp.team_selection_id = ts.team_selection_id
            JOIN user u ON u.user_id = tsp.user_id
            WHERE ts.fixture_id = %s
            ORDER BY tsp.pair_number ASC, tsp.selection_order ASC
        """

        value = (fixture_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        players = []
        for row in results:
            players.append({
                "user_id": row[0],
                "pair_number": row[1],
                "selection_order": row[2],
                "firstname": row[3],
                "surname": row[4],
            })

        return players
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the results for a fixture - requires user_id
def get_result_of_fixture_for_one_user(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.start_time, f.location, f.is_home, f.division, f.notes, m.match_id, m.pair_number, m.did_win, m.sets_won, m.sets_lost, m.games_won, m.games_lost
            FROM fixture f
            JOIN squad_players sp ON sp.squad_id = f.squad_id
            JOIN `match` m ON m.fixture_id = f.fixture_id
            JOIN match_players mp ON mp.match_id = m.match_id
            JOIN user u ON u.user_id = mp.user_id
            WHERE sp.user_id = %s AND mp.user_id = %s AND f.date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND f.date <= CURDATE()
            GROUP BY m.match_id
            ORDER BY f.date DESC, m.pair_number
        """

        values = (user_id, user_id)

        cursor.execute(sql, values)
        SQL_results = cursor.fetchall()

        cursor.close()
        connection.close()

        results = []
        for row in SQL_results:
            results.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[5] else "Away"),
                "division" : row[6],
                "notes" : row[7],
                "match_id" : row[8],
                "pair_number" : row[9],
                "did_win" : bool(row[10]),
                "sets_won" : row[11],
                "sets_lost" : row[12],
                "games_won" : row[13],
                "games_lost" : row[14]
            })

        return results
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get partner feedback for one fixture - requires fixture_id and user_id
def get_partner_feedback_for_one_fixture(fixture_id: int, user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT f.opponent_name, f.date, f.is_home, pf.overall_rating, pf.key_moments_rating, pf.communication_rating, pf.comments
        FROM  partner_feedback pf
        JOIN `match` m ON m.match_id = pf.match_id
        JOIN fixture f ON f.fixture_id = m.fixture_id
        WHERE m.fixture_id = %s AND pf.reviewed_id = %s
        """

        values = (fixture_id, user_id)

        cursor.execute(sql, values)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        feedback = []
        for row in results:
            feedback.append({
                "opposition" : row[0],
                "date" : row[1].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[2] else "Away"),
                "overall_rating" : row[3],
                "key_moments_rating" : row[4],
                "communication_rating" : row[5],
                "comments" : row[6]
            })

        return feedback
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get recent partner feedback for one user - requires user_id
def get_recent_partner_feedback(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT f.opponent_name, f.date, f.is_home, pf.overall_rating, pf.key_moments_rating, pf.communication_rating, pf.comments
        FROM  partner_feedback pf
        JOIN `match` m ON m.match_id = pf.match_id
        JOIN fixture f ON f.fixture_id = m.fixture_id
        WHERE pf.reviewed_id = %s AND f.date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND f.date <= CURDATE()
        ORDER BY f.date DESC
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        feedback = []
        for row in results:
            feedback.append({
                "opposition" : row[0],
                "date" : row[1].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[2] else "Away"),
                "overall_rating" : row[3],
                "key_moments_rating" : row[4],
                "communication_rating" : row[5],
                "comments" : row[6]
            })

        return feedback
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get see if a user has submitted partner feedback - requires fixture_id and user_id
def has_submitted_feedback(fixture_id: int, user_id: int) -> bool:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT 1
        FROM  partner_feedback pf
        JOIN `match` m ON m.match_id = pf.match_id
        WHERE m.fixture_id = %s AND pf.reviewer_id = %s
        """

        values = (fixture_id, user_id)

        cursor.execute(sql, values)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        return results is not None
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the name of a partner for a fixture - requires user_id and match_id
def get_partner_info(user_id: int, match_id: int) -> dict:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT u.first_name, u.surname, u.user_id
        FROM match_players mp
        JOIN user u ON u.user_id = mp.partner_user_id
        WHERE mp.match_id = %s AND mp.user_id = %s
        """

        values = (match_id, user_id)

        cursor.execute(sql, values)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        partner_info = {
            "firstname": result[0],
            "surname": result[1],
            "user_id": result[2]
        }
        return partner_info
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to insert partner feedback for a fixture
def insert_partner_feedback(match_id: int, reviewer_id: int, reviewed_id: int, overall_rating: int, key_moments_rating: int, communication_rating: int, comments: str) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        INSERT INTO partner_feedback
        (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date.today())

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get a players injury status - requires user_id
def get_injury_info(user_id) -> dict:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT injury_id, description, expected_end_date, is_current, notes, can_play
        FROM injury
        WHERE user_id = %s AND is_current = 1
        """

        values = (user_id,)

        cursor.execute(sql, values)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        if results == None:
            return None

        injury_info = {
            "injury_id": results[0],
            "description": results[1],
            "expected_end_date": results[2],
            "is_current": results[3],
            "notes": results[4],
            "can_play": results[5]
        }
        return injury_info
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to change the is_current injury to 0 from 1 - requires injury_id
def remove_injury_status(injury_id: int) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            UPDATE injury
            SET is_current = 0
            WHERE injury_id = %s
        """

        value = (injury_id,)

        cursor.execute(sql, value)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to update the injury status row for the member
def update_injury_status(injury_id: int, description: str, expected_end_date: date, can_play: bool, notes: str) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            UPDATE injury
            SET description = %s, expected_end_date = %s, notes = %s, can_play = %s
            WHERE injury_id = %s
        """
        values = (description, expected_end_date, notes, can_play, injury_id)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to add an injury status
def insert_injury_status(user_id: int, description: str, expected_end_date: date, can_play: bool, notes: str) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            INSERT into injury
            (user_id, description, start_date, expected_end_date, is_current, notes, can_play)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (user_id, description, date.today(), expected_end_date, True, notes, can_play)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get player details for one squad - requires user_id
def get_players_in_one_squad(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT u.user_id, u.first_name, u.surname, d.division_name, COUNT(mp.match_id) AS games_played, SUM(m.did_win) AS wins, MAX(m.date) AS last_match_date, MAX(i.description) AS injury_description, COUNT(DISTINCT CASE WHEN s.is_current = 1 THEN m.fixture_id ELSE NULL END) AS fixtures_played_this_season
            FROM squad_players sp
            JOIN `user` u ON u.user_id = sp.user_id
            JOIN squad sq ON sq.squad_id = sp.squad_id
            JOIN division d on d.division_id = sq.division_id
            LEFT JOIN match_players mp ON mp.user_id = u.user_id
            LEFT JOIN `match` m ON m.match_id = mp.match_id
            LEFT JOIN fixture f ON f.fixture_id = m.fixture_id
            LEFT JOIN season s ON s.season_id = f.season_id
            LEFT JOIN injury i ON i.user_id = u.user_id AND i.is_current = 1
            WHERE sp.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1)
            GROUP BY u.user_id, u.first_name, u.surname, d.division_name
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()

        players = []
        for row in results:
            games_played = row[4]
            wins = row[5] if row[5] is not None else 0
            win_loss_percentage = round((wins / games_played) * 100, 1) if games_played > 0 else 0

            players.append({
                "user_id": row[0],
                "firstname": row[1],
                "surname": row[2],
                "division_name": row[3],
                "games_played": games_played,
                "win_percentage": win_loss_percentage,
                "last_match_date": row[6],
                "injury_description": row[7],
                "fixtures_played_this_season": row[8]
            })

        return players
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the data from matches within the last 3 years for 1 user - requires user_id, a date to check before
def get_match_history_last_three_years(user_id: int, before_date: date) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT m.match_id, m.date, m.games_won, m.games_lost, mp.partner_form_at_match, f.opponent_league_position, d.team_count, f.season_id
            FROM `match` m
            JOIN match_players mp ON mp.match_id = m.match_id
            JOIN fixture f ON f.fixture_id = m.fixture_id
            LEFT JOIN division d on d.division_id = f.division
            WHERE mp.user_id = %s AND m.date >= %s AND m.date < %s
            ORDER BY m.date ASC
        """

        values = (user_id, (date.today() - relativedelta(years=3)), before_date)

        cursor.execute(sql, values)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        matches = []
        for row in results:
            matches.append({
                "match_id": row[0],
                "date": row[1],
                "games_won": row[2],
                "games_lost": row[3],
                "partner_form_at_match": float(row[4]) if row[4] is not None else None,
                "opponent_league_position": row[5],
                "division_team_count": row[6],
                "season_id": row[7]
            })

        return matches
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to count how fixtures there has been in a season up to a certain date - requires season_id, before_date
def count_fixtures_before_date(season_id: int, before_date: date) -> int:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT COUNT(f.fixture_id) as amount_fixtures
            FROM fixture f
            WHERE f.season_id = %s AND f.date < %s AND EXISTS (SELECT 1 FROM `match` m WHERE m.fixture_id = f.fixture_id)
        """

        values = (season_id, before_date)

        cursor.execute(sql, values)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        return results[0]
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to return all available players for a fixture - requires fixture_id
def get_all_available_players(fixture_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT u.user_id, u.first_name, u.surname
            FROM availability a
            JOIN user u ON a.user_id = u.user_id
            LEFT JOIN injury i ON a.user_id = i.user_id AND i.is_current = 1
            WHERE a.fixture_id = %s AND a.is_available = 1 AND (i.injury_id IS NULL OR i.can_play = 1)
        """

        value = (fixture_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        players = []
        for row in results:
            players.append({
                "user_id": row[0],
                "firstname": row[1],
                "surname": row[2]
            })

        return players
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to count how many times a player has played with another player
def count_partnership_matches(player_id: int, partner_id: int) -> int:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT COUNT(mp.match_player_id) as times_played
            FROM match_players mp
            JOIN `match` m ON mp.match_id = m.match_id
            WHERE mp.user_id = %s AND mp.partner_user_id = %s AND m.date >= %s
        """

        values = (player_id, partner_id, (date.today() - relativedelta(years=3)))

        cursor.execute(sql, values)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        return results[0]
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the last 10 feedback scores about a user - requires user_id
def get_last_ten_feedback_scores(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT overall_rating, key_moments_rating, communication_rating, date
            FROM partner_feedback pf
            WHERE reviewed_id = %s
            ORDER BY date DESC
            LIMIT 10
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        feedback_scores = []
        for row in results:
            feedback_scores.append({
                "overall_rating": row[0],
                "key_moments_rating": row[1],
                "communication_rating": row[2]
            })

        feedback_scores.reverse()

        return feedback_scores
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get information aboubt all players from the captains squad ranking and below - requires user_id, club_id, squad_ranking
def get_all_players_for_squads_below_ranking(user_id: int, club_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT u.user_id, u.first_name, u.surname, d.division_name, COUNT(mp.match_id) AS games_played, SUM(m.did_win) AS wins, MAX(m.date) AS last_match_date, MAX(i.description) AS injury_description, COUNT(DISTINCT CASE WHEN s.is_current = 1 THEN m.fixture_id ELSE NULL END) AS fixtures_played_this_season
            FROM squad_players sp
            JOIN `user` u ON u.user_id = sp.user_id
            JOIN squad sq ON sq.squad_id = sp.squad_id
            JOIN division d ON d.division_id = sq.division_id
            LEFT JOIN match_players mp ON mp.user_id = u.user_id
            LEFT JOIN `match` m ON m.match_id = mp.match_id
            LEFT JOIN fixture f ON f.fixture_id = m.fixture_id
            LEFT JOIN season s ON s.season_id = f.season_id
            LEFT JOIN injury i ON i.user_id = u.user_id AND i.is_current = 1
            WHERE sq.squad_ranking > (
                SELECT sq2.squad_ranking
                FROM squad_players sp2
                JOIN squad sq2 ON sq2.squad_id = sp2.squad_id
                WHERE sp2.user_id = %s
                LIMIT 1
                ) AND u.club_id = %s
            GROUP BY u.user_id, u.first_name, u.surname, d.division_name
        """

        values = (user_id, club_id)

        cursor.execute(sql, values)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        players = []
        for row in results:
            games_played = row[4]
            wins = row[5] if row[5] is not None else 0
            win_loss_percentage = round((wins / games_played) * 100, 1) if games_played > 0 else 0

            players.append({
                "user_id": row[0],
                "firstname": row[1],
                "surname": row[2],
                "division_name": row[3],
                "games_played": games_played,
                "win_percentage": win_loss_percentage,
                "last_match_date": row[6],
                "injury_description": row[7],
                "fixtures_played_this_season": row[8]
            })

        return players
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get a user's club_id - requires user_id
def get_club_id(user_id: int) -> int:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT club_id
            FROM `user`
            WHERE user_id = %s
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchone()

        cursor.close()
        connection.close()

        return results[0]
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        
        
#Function to add a player to the captain's squad - requires user_id and player_id
def add_player_to_squad(captain_id: int, player_id: int) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            UPDATE squad_players sp
            JOIN squad_players cap ON cap.user_id = %s
            SET sp.squad_id = cap.squad_id
            WHERE sp.user_id = %s
        """

        values = (captain_id, player_id)

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        
        
#Function to get the results of every match for the captain's squad this season - requires user_id
def get_squad_results(captain_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.is_home, SUM(m.sets_won) AS total_sets_won, SUM(m.sets_lost) AS total_sets_lost
            FROM fixture f
            JOIN `match` m ON m.fixture_id = f.fixture_id
            JOIN season s ON s.season_id = f.season_id
            WHERE f.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1)
            AND s.is_current = 1
            GROUP BY f.fixture_id, f.opponent_name, f.date, f.is_home
            ORDER BY f.date DESC
        """

        value = (captain_id,)

        cursor.execute(sql, value)
        SQL_results = cursor.fetchall()

        cursor.close()
        connection.close()

        results = []
        for row in SQL_results:
            sets_won = int(row[4])
            sets_lost = int(row[5])
            results.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[3] else "Away"),
                "did_win" : sets_won > sets_lost,
                "sets_won" : sets_won,
                "sets_lost" : sets_lost
            })

        return results
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the upcoming fixtures for the captain's squad this season - requires user_id
def get_squad_upcoming_fixtures(captain_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.is_home
            FROM fixture f
            JOIN season s ON s.season_id = f.season_id
            WHERE f.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1)
            AND s.is_current = 1
            AND f.date >= CURDATE()
            ORDER BY f.date ASC, f.start_time ASC
        """

        value = (captain_id,)

        cursor.execute(sql, value)
        SQL_results = cursor.fetchall()

        cursor.close()
        connection.close()

        fixtures = []
        for row in SQL_results:
            fixtures.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[3] else "Away")
            })

        return fixtures
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get all information for one fixture - requires fixture_id
def get_fixture_information(fixture_id: int) -> dict:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT opponent_name, date, start_time, location, is_home, opponent_league_position, notes
            FROM fixture
            WHERE fixture_id = %s
        """

        value = (fixture_id,)

        cursor.execute(sql, value)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return {
                "opponent_name": result[0],
                "date": result[1].strftime("%d/%m/%Y"),
                "start_time": format_time(result[2]),
                "location": result[3],
                "is_home": bool(result[4]),
                "opponent_league_position": result[5],
                "notes": result[6]
            }
        return None
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to save the players for a fixture using an open cursor, requires fixture_id, players
def save_team_selection_players(cursor, fixture_id: int, players: list[dict]) -> None:
    cursor.execute("SELECT team_selection_id FROM team_selection WHERE fixture_id = %s", (fixture_id,))
    existing = cursor.fetchone()

    if existing is not None:
        team_selection_id = existing[0]

        cursor.execute("""
            UPDATE team_selection
            SET date = %s
            WHERE team_selection_id = %s
        """, (date.today(), team_selection_id))

        cursor.execute("DELETE FROM team_selection_players WHERE team_selection_id = %s", (team_selection_id,))
    else:
        cursor.execute("""
            INSERT INTO team_selection
            (fixture_id, date)
            VALUES (%s, %s)
        """, (fixture_id, date.today()))

        team_selection_id = cursor.lastrowid

    sql = """
        INSERT INTO team_selection_players
        (team_selection_id, user_id, pair_number, selection_order)
        VALUES (%s, %s, %s, %s)
    """

    for player in players:
        cursor.execute(sql, (team_selection_id, player["user_id"], player["pair_number"], player["selection_order"]))


#Function to update the information for one fixture and its selected players - requires all fields shown on the add/edit fixture screen
def update_fixture(fixture_id: int, opponent_name: str, fixture_date: date, start_time: str, location: str, is_home: bool, opponent_league_position: int, notes: str | None = None, players: list[dict] | None = None) -> None:
    connection = None
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            UPDATE fixture
            SET opponent_name = %s, date = %s, start_time = %s, location = %s, is_home = %s,
                opponent_league_position = %s, notes = %s
            WHERE fixture_id = %s
        """

        values = (opponent_name, fixture_date, start_time, location, is_home, opponent_league_position, notes, fixture_id)

        cursor.execute(sql, values)

        if players is not None:
            save_team_selection_players(cursor, fixture_id, players)

        #The fixture and the players are committed together
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        if connection is not None:
            connection.rollback()
            connection.close()


#Function to insert a fixture and its selected players for the captain's squad and the current season - requires all fields shown on the add/edit fixture screen
def insert_fixture(captain_id: int, opponent_name: str, fixture_date: date, start_time: str, location: str, is_home: bool, opponent_league_position: int | None, notes: str | None = None, players: list[dict] | None = None) -> int:
    connection = None
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            INSERT INTO fixture
            (created_by_id, opponent_name, date, start_time, location, is_home, division,
            opponent_league_position, notes, squad_id, season_id)
            SELECT %s, %s, %s, %s, %s, %s, sq.division_id, %s, %s, sq.squad_id, s.season_id
            FROM squad_players sp
            JOIN squad sq ON sq.squad_id = sp.squad_id
            JOIN season s ON s.is_current = 1
            WHERE sp.user_id = %s
            LIMIT 1
        """

        values = (captain_id, opponent_name, fixture_date, start_time, location, is_home,
                  opponent_league_position, notes, captain_id)

        cursor.execute(sql, values)

        new_fixture_id = cursor.lastrowid if cursor.rowcount == 1 else None

        #The players can only be added if the fixture was actually inserted
        if new_fixture_id is not None and players is not None:
            save_team_selection_players(cursor, new_fixture_id, players)

        #The fixture and the players are committed together
        connection.commit()

        cursor.close()
        connection.close()

        return new_fixture_id
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        if connection is not None:
            connection.rollback()
            connection.close()


#Function to remove a fixture - requires fixture_id
def remove_fixture(fixture_id: int) -> None:
    connection = None
    try:
        connection = connect_database()
        cursor = connection.cursor()

        value = (fixture_id,)

        #Remove the players picked for the fixture's team selection
        sql = """
            DELETE tsp
            FROM team_selection_players tsp
            JOIN team_selection ts ON ts.team_selection_id = tsp.team_selection_id
            WHERE ts.fixture_id = %s
        """
        cursor.execute(sql, value)

        #Remove the team selection itself
        sql = """
            DELETE FROM team_selection
            WHERE fixture_id = %s
        """
        cursor.execute(sql, value)

        #Remove the availability submitted for the fixture
        sql = """
            DELETE FROM availability
            WHERE fixture_id = %s
        """
        cursor.execute(sql, value)

        #Remove the fixture
        sql = """
            DELETE FROM fixture
            WHERE fixture_id = %s
        """
        cursor.execute(sql, value)

        #Nothing is saved until every delete has worked
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        if connection is not None and connection.is_connected():
            connection.rollback()
            connection.close()


#Function to get the fixtures which have been played but do not have any match results yet - requires user_id (the captain's)
def get_fixtures_without_results(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.start_time, f.location, f.is_home, f.division, f.notes
            FROM fixture f
            WHERE f.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1)
            AND f.date < CURDATE()
            AND NOT EXISTS (
                SELECT 1
                FROM `match` m
                WHERE m.fixture_id = f.fixture_id
            )
            ORDER BY f.date ASC, f.start_time ASC
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        fixtures = []
        for row in results:
            fixtures.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "start_time" : format_time(row[3]),
                "location" : row[4],
                "home_away" : ("Home" if row[5] else "Away"),
                "division" : row[6],
                "notes" : row[7]
            })

        return fixtures
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")