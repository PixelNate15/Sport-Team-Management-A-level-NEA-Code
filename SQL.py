import mysql.connector
from home_ip import getHomeIP
from datetime import datetime, date

#Function to covert the timedelta into time
def format_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


#Function to connect to the database
def connect_database():
    try:
        connection = mysql.connector.connect(
            host=getHomeIP(),
            user="alevel_user",
            password="b6ZMUxyMrEdPU1oSjJfLRFBvTOVJWH7h",
            database="alevel_app"
        )

        return connection

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None


#Function to get the user_id of a user from the db from their username - requires username
def get_user_id(username: str) -> int:
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

    cursor.execute(sql, values)
    connection.commit()

    new_user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return new_user_id


#Function to check that a username is not already in the db - requires username
def check_for_duplicate_username(username: str) -> bool:
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


#Function to get the password hash from the db for a certain username - requires username
def check_password_hash(username: str) -> str:
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
    

#Function to check whether a user is a coach or a normal member - requires user_id
def check_is_captain(user_id: int) -> bool:
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


#Function to get all fixtures for a user for the team that they are involved in - requires user_id
def get_fixtures(user_id: int) -> list[dict]:
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
        ORDER BY f.date ASC, f.start_time ASC
    """
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


#Function to insert the availability of a member for a fixture - requires fixture_id,  user_id, is_available and an optional variable of reason
def insert_availability_details(fixture_id: int, user_id: int, is_available: bool, reason: str | None = None):
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
    
    
#Function to get the pair and players for a fixture - requires fixture_id
def get_players_for_fixture(fixture_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
        SELECT tsp.pair_number, u.first_name, u.surname
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
            "pair_number": row[0],
            "firstname": row[1],
            "surname": row[2]
        })
    
    return players
