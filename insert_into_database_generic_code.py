import mysql.connector
from home_ip import getHomeIP

USER_COLUMNS = []
USER_DATA = []

SQUAD_COLUMNS = []
SQUAD_DATA = []

FIXTURE_COLUMNS = []
FIXTURE_DATA = []

AVAILABILITY_COLUMNS = []
AVAILABILITY_DATA = []

FORM_COLUMNS = []
FORM_DATA = []

INJURY_COLUMNS = []
INJURY_DATA = []

MATCH_COLUMNS = []
MATCH_DATA = []

MATCH_PLAYER_COLUMNS = []
MATCH_PLAYER_DATA = []

FEEDBACK_COLUMNS = []
FEEDBACK_DATA = []

SETTINGS_COLUMNS = []
SETTINGS_DATA = []

SQUAD_PLAYERS_COLUMNS = []
SQUAD_PLAYERS_DATA = []

TEAM_SELECTION_COLUMNS = []
TEAM_SELECTION_DATA = []

TEAM_SELECTION_PLAYERS_COLUMNS = []
TEAM_SELECTION_PLAYERS_DATA = []


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

#The tables are placed in order for insertion, since the first table inserted shouldn't have any foreign keys
TABLES = {
    "user": (USER_COLUMNS, USER_DATA),
    "squad": (SQUAD_COLUMNS, SQUAD_DATA),
    "fixture": (FIXTURE_COLUMNS, FIXTURE_DATA),
    "availability": (AVAILABILITY_COLUMNS, AVAILABILITY_DATA),
    "form": (FORM_COLUMNS, FORM_DATA),
    "injury": (INJURY_COLUMNS, INJURY_DATA),
    "match": (MATCH_COLUMNS, MATCH_DATA),
    "match_player": (MATCH_PLAYER_COLUMNS, MATCH_PLAYER_DATA),
    "feedback": (FEEDBACK_COLUMNS, FEEDBACK_DATA),
    "settings": (SETTINGS_COLUMNS, SETTINGS_DATA),
    "squad_players": (SQUAD_PLAYERS_COLUMNS, SQUAD_PLAYERS_DATA),
    "team_selection": (TEAM_SELECTION_COLUMNS, TEAM_SELECTION_DATA),
    "team_selection_players": (TEAM_SELECTION_PLAYERS_COLUMNS, TEAM_SELECTION_PLAYERS_DATA)
}


#Function to load the test data
def load_test_data():
    connection = connect_database()
    cursor = connection.cursor()
    
    # Delete existing data in reverse order to avoid foreign key errors
    for table in reversed(TABLES):
        cursor.execute(f"DELETE FROM `{table}`")

    # Insert test data into each table
    for table, (columns, records) in TABLES.items():
        column_names = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        sql = f"INSERT INTO `{table}` ({column_names}) VALUES ({placeholders})"

        for record in records:
            cursor.execute(sql, record)


    connection.commit()
    
    cursor.close()
    connection.close()


load_test_data()