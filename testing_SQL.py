import mysql.connector
from home_ip import getHomeIP
from datetime import datetime

#Function to connect to the database
def connect_database():
    try:
        myIP = getHomeIP()
        username = "alevel_user"
        password = "b6ZMUxyMrEdPU1oSjJfLRFBvTOVJWH7h"
        # myIP = "localhost"
        # username = "root"
        # password = ""
        connection = mysql.connector.connect(
            host=myIP,
            user=username,
            password=password,
            database="alevel_app"
        )

        return connection

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None
    
#Function to add the information from the create account screen to the db, return the userID for easy transferring to the main screen
def insert_account_details(firstname: str, surname: str, date_of_birth: datetime, username: str, password_hash: str, email: str) -> int:
    connection = connect_database()
    cursor = connection.cursor()

    sql = """
        INSERT into user
        (first_name, surname, username, password_hash, date_of_birth, is_captain, email, is_active)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (firstname, surname, username, password_hash, date_of_birth, False, email, True)

    try:
        cursor.execute(sql, values)
        connection.commit()

        new_user_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return new_user_id
    
    except Exception as err:
        return None


firstname = input("What is the firstname you want to test? ")
surname = input("What is the surname you want to test? ")
username = input("What is the username you want to test? ")
password_hash = input("What is the password hash you want to test? ")
email = input("What is the email you want to test? ")
date_of_birth = input("What is the date of birth? (YYYY-MM-DD): ")

# Insert the account into the database
new_user_id = insert_account_details(
    firstname,
    surname,
    date_of_birth,
    username,
    password_hash,
    email
)

# Display the result
print(f"Account unsuccessfully created with User ID: {new_user_id}")