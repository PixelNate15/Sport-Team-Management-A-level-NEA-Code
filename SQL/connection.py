import mysql.connector

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
