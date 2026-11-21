import mysql.connector
from datetime import datetime
from SQL.connection import connect_database

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
