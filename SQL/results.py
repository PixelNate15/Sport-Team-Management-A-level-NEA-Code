import mysql.connector
from datetime import date
from SQL.connection import connect_database

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
            did_win = True if sets_won > sets_lost else False
            results.append({
                "fixture_id" : row[0],
                "opposition" : row[1],
                "date" : row[2].strftime("%d/%m/%Y"),
                "home_away" : ("Home" if row[3] else "Away"),
                "did_win" : did_win,
                "sets_won" : sets_won,
                "sets_lost" : sets_lost
            })

        return results
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get a result - requires fixture_id
def get_result(fixture_id: int) -> dict | None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.opponent_name, f.date, f.is_home, d.division_name, f.notes
            FROM fixture f
            LEFT JOIN division d ON d.division_id = f.division
            LEFT JOIN `match` m ON m.fixture_id = f.fixture_id
            LEFT JOIN match_players mp ON mp.match_id = m.match_id
            LEFT JOIN user u ON u.user_id = mp.user_id
            WHERE f.fixture_id = %s
            GROUP BY f.fixture_id, f.opponent_name, f.date, f.is_home, d.division_name, f.notes
        """

        cursor.execute(sql, (fixture_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result is not None:
            return {
                "opposition": result[0],
                "date": result[1],
                "home_away" : ("Home" if result[2] else "Away"),
                "division": result[3],
                "notes": result[4],
            }
        return None

    except ConnectionError:
        print("ERROR: Could not connect to database")
    
    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        return None


#Function to get the saved matches for a fixture - requires fixture_id
def get_matches_for_fixture(fixture_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT match_id, pair_number, set_1_won, set_1_lost, set_2_won, set_2_lost, champ_tie
            FROM `match`
            WHERE fixture_id = %s
            ORDER BY match_id ASC
        """

        value = (fixture_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        matches = []
        for row in results:
            matches.append({
                "match_id": row[0],
                "pair_number": row[1],
                "set_1_won": row[2],
                "set_1_lost": row[3],
                "set_2_won": row[4],
                "set_2_lost": row[5],
                "champ_tie": row[6]
            })

        return matches
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to add or edit one match and its players - requires fixture_id, fixture date, a match dict, and a flag for if its new
def save_match(fixture_id: int, fixture_date: date, match: dict, is_new: bool) -> bool:
    connection = None
    try:
        connection = connect_database()
        cursor = connection.cursor()

        if is_new:
            sql = """
                INSERT INTO `match`
                (pair_number, opponent_pair_number, date, did_win, sets_won, sets_lost, games_won, games_lost,
                set_1_won, set_1_lost, set_2_won, set_2_lost, champ_tie, fixture_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        else:
            sql = """
                UPDATE `match`
                SET pair_number = %s, opponent_pair_number = %s, date = %s, did_win = %s,
                    sets_won = %s, sets_lost = %s, games_won = %s, games_lost = %s,
                    set_1_won = %s, set_1_lost = %s, set_2_won = %s, set_2_lost = %s, champ_tie = %s
                WHERE match_id = %s
            """

        #The last value is the fixture_id when inserting and the match_id when updating
        values = (match["pair_number"], match["opponent_pair_number"], fixture_date, match["sets_won"] > match["sets_lost"], match["sets_won"], match["sets_lost"], match["games_won"], match["games_lost"], match["set_1_won"], match["set_1_lost"], match ["set_2_won"], match["set_2_lost"], match["champ_tie"], fixture_id if is_new else match["match_id"])

        cursor.execute(sql, values)
        match_id = cursor.lastrowid if is_new else match["match_id"]

        save_match_players(cursor, match_id, match)

        connection.commit()

        cursor.close()
        connection.close()
        return True
    except ConnectionError:
        print("ERROR: Could not connect to database")
        return False

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        if connection is not None and connection.is_connected():
            connection.rollback()
            connection.close()
        return False


#Function to save the two players of one match using an open cursor - requires match_id and the match dict
def save_match_players(cursor, match_id: int, match: dict) -> None:
    #Any existing player rows are removed first so an edited match is never left with old players
    cursor.execute("""
        DELETE FROM match_players
        WHERE match_id = %s
    """, (match_id,))

    sql = """
        INSERT INTO match_players
        (match_id, user_id, partner_user_id, partner_form_at_match)
        VALUES (%s, %s, %s, %s)
    """

    #Each player's row stores their partner's form at the time of the match
    cursor.execute(sql, (match_id, match["player_1"], match["player_2"], match["form_2"]))
    cursor.execute(sql, (match_id, match["player_2"], match["player_1"], match["form_1"]))
