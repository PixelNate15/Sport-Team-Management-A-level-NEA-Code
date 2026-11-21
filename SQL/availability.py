import mysql.connector
from datetime import date
from SQL.connection import connect_database

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
