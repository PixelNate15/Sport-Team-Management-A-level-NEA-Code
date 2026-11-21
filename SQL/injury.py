import mysql.connector
from datetime import date
from SQL.connection import connect_database

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
