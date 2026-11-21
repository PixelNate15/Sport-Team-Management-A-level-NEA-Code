import mysql.connector
from SQL.connection import connect_database

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


#Function to get information aboubt all players from the captains squad ranking and below - requires user_id and club_id
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


#Function to move a player down to the squad below their current squad - requires player_id
def remove_player_from_squad(player_id: int) -> bool:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            UPDATE squad_players sp
            JOIN squad current_squad ON current_squad.squad_id = sp.squad_id
            JOIN squad lower_squad ON lower_squad.club_id = current_squad.club_id
            SET sp.squad_id = lower_squad.squad_id
            WHERE sp.user_id = %s
            AND lower_squad.squad_ranking = (
                SELECT MIN(s.squad_ranking)
                FROM squad s
                WHERE s.club_id = current_squad.club_id AND s.squad_ranking > current_squad.squad_ranking
            )
        """

        value = (player_id,)

        cursor.execute(sql, value)
        connection.commit()

        was_moved = cursor.rowcount > 0

        cursor.close()
        connection.close()

        return was_moved
    except ConnectionError:
        print("ERROR: Could not connect to database")
        return False

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
        return False