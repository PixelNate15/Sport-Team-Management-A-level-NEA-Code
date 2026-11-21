import mysql.connector
from datetime import date
from SQL.connection import connect_database, format_time

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


#Function to get the upcoming fixtures for the captain's squad this season - requires user_id
def get_squad_upcoming_fixtures(captain_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT f.fixture_id, f.opponent_name, f.date, f.is_home
            FROM fixture f
            JOIN season s ON s.season_id = f.season_id
            WHERE f.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1) AND s.is_current = 1 AND f.date >= CURDATE()
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


#Function to get the fixtures which have been played but do not have any match results yet - requires user_id
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


#Function to insert a fixture and its selected players for the captain's squad and the current season - requires all fields shown on the add/edit fixture screen
def insert_fixture(captain_id: int, opponent_name: str, fixture_date: date, start_time: str, location: str, is_home: bool, opponent_league_position: int | None, notes: str | None = None, players: list[dict] | None = None) -> int:
    connection = None
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            INSERT INTO fixture
            (created_by_id, opponent_name, date, start_time, location, is_home, division, opponent_league_position, notes, squad_id, season_id)
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


#Function to save the players for a fixture using an open cursor, requires fixture_id, players
def save_team_selection_players(cursor, fixture_id: int, players: list[dict]) -> None:
    cursor.execute("""
        SELECT team_selection_id
        FROM team_selection
        WHERE fixture_id = %s
    """, (fixture_id,))
    
    existing = cursor.fetchone()

    if existing is not None:
        team_selection_id = existing[0]

        cursor.execute("""
            UPDATE team_selection
            SET date = %s
            WHERE team_selection_id = %s
        """, (date.today(), team_selection_id))

        cursor.execute("""
            DELETE FROM team_selection_players
            WHERE team_selection_id = %s
        """, (team_selection_id,))
        
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
