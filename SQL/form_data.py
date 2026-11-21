import mysql.connector
from datetime import date
from dateutil.relativedelta import relativedelta
from SQL.connection import connect_database

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
