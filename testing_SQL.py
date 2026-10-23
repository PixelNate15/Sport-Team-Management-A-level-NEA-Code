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
    
    