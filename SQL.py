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
def insert_availability_details(fixture_id: int, user_id: int, is_available: bool, reason: str | None = None) -> None:
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


#Function to get the results for a fixture - requires user_id
def get_result_of_fixture_for_one_user(user_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
        SELECT f.fixture_id, f.opponent_name, f.date, f.start_time, f.location, f.is_home, f.division, f.notes, m.match_id, m.pair_number, m.did_win, m.sets_won, m.sets_lost, m.games_won, m.games_lost
        FROM fixture f
        JOIN squad_players sp ON sp.squad_id = f.squad_id
        JOIN `match` m ON m.fixture_id = f.fixture_id
        JOIN match_players mp ON mp.match_id = m.match_id
        JOIN user u ON u.user_id = mp.user_id
        WHERE sp.user_id = %s AND mp.user_id = %s AND f.date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND f.date <= CURDATE()
        GROUP BY m.match_id
        ORDER BY f.date DESC, m.pair_number
    """
    
    values = (user_id, user_id)
    
    cursor.execute(sql, values)
    SQL_results = cursor.fetchall()
        
    cursor.close()
    connection.close()
    
    results = []
    for row in SQL_results:
        results.append({
            "fixture_id" : row[0],
            "opposition" : row[1],
            "date" : row[2].strftime("%d/%m/%Y"),
            "home_away" : ("Home" if row[5] else "Away"),
            "division" : row[6],
            "notes" : row[7],
            "match_id" : row[8],
            "pair_number" : row[9],
            "did_win" : bool(row[10]),
            "sets_won" : row[11],
            "sets_lost" : row[12],
            "games_won" : row[13],
            "games_lost" : row[14]
        })
    
    return results


#Function to get partner feedback for one fixture - requires fixture_id and user_id
def get_partner_feedback_for_one_fixture(fixture_id: int, user_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
    SELECT f.opponent_name, f.date, f.is_home, pf.overall_rating, pf.key_moments_rating, pf.communication_rating, pf.comments
    FROM  partner_feedback pf
    JOIN `match` m ON m.match_id = pf.match_id
    JOIN fixture f ON f.fixture_id = m.fixture_id
    WHERE m.fixture_id = %s AND pf.reviewed_id = %s
    """
    
    values = (fixture_id, user_id)

    cursor.execute(sql, values)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    
    feedback = []
    for row in results:
        feedback.append({
            "opposition" : row[0],
            "date" : row[1].strftime("%d/%m/%Y"),
            "home_away" : ("Home" if row[2] else "Away"),
            "overall_rating" : row[3],
            "key_moments_rating" : row[4],
            "communication_rating" : row[5],
            "comments" : row[6]
        })
        
    return feedback


#Function to get recent partner feedback for one user - requires user_id
def get_recent_partner_feedback(user_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
    SELECT f.opponent_name, f.date, f.is_home, pf.overall_rating, pf.key_moments_rating, pf.communication_rating, pf.comments
    FROM  partner_feedback pf
    JOIN `match` m ON m.match_id = pf.match_id
    JOIN fixture f ON f.fixture_id = m.fixture_id
    WHERE pf.reviewed_id = %s
    AND f.date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    AND f.date <= CURDATE()
    ORDER BY f.date DESC
    """
    
    value = (user_id,)

    cursor.execute(sql, value)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    
    feedback = []
    for row in results:
        feedback.append({
            "opposition" : row[0],
            "date" : row[1].strftime("%d/%m/%Y"),
            "home_away" : ("Home" if row[2] else "Away"),
            "overall_rating" : row[3],
            "key_moments_rating" : row[4],
            "communication_rating" : row[5],
            "comments" : row[6]
        })
        
    return feedback


#Function to get see if a user has submitted partner feedback - requires fixture_id and user_id
def has_submitted_feedback(fixture_id: int, user_id: int) -> bool:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
    SELECT pf.overall_rating
    FROM  partner_feedback pf
    JOIN `match` m ON m.match_id = pf.match_id
    WHERE m.fixture_id = %s AND pf.reviewer_id = %s
    """
    
    values = (fixture_id, user_id)

    cursor.execute(sql, values)
    results = cursor.fetchone()

    cursor.close()
    connection.close()
    
    return results is not None


#Function to get the name of a partner for a fixture - requires user_id and match_id
def get_partner_info(user_id: int, match_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
    SELECT u.first_name, u.surname, u.user_id
    FROM match_players mp
    JOIN user u ON u.user_id = mp.partner_user_id
    WHERE mp.match_id = %s AND mp.user_id = %s
    """
    
    values = (match_id, user_id)

    cursor.execute(sql, values)
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    
    partner_info = {
        "firstname": result[0],
        "surname": result[1],
        "user_id": result[2]
    }
    return partner_info


#Function to insert partner feedback for a fixture
def insert_partner_feedback(match_id: int, reviewer_id: int, reviewed_id: int, overall_rating: int, key_moments_rating: int, communication_rating: int, comments: str) -> None:
    connection = connect_database()
    cursor = connection.cursor()
    
    sql = """
    INSERT INTO partner_feedback
    (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date.today())

    print(sql.count("%s"), len(values))
    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()
    
    
#Function to get a players injury status - requires user_id
def get_injury_info(user_id) -> dict:
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


#Function to change the is_current injury to 0 from 1 - requires injury_id
def remove_injury_status(injury_id: int) -> None:
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
    
    
#Function to update the injury status row for the member
def member_update_injury_status(injury_id: int, description: str, expected_end_date: date, can_play: bool, notes: str) -> None:
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
    
    
#Function to update the injury status row for the captain
def captain_update_injury_status(injury_id: int, injury_weighting: float) -> None:
    connection = connect_database()
    cursor = connection.cursor()

    sql = """
        UPDATE injury
        SET injury_weighting = %s
        WHERE injury_id = %s
    """
    values = (injury_weighting, injury_id)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()
    
    
#Function to add an injury status
def insert_injury_status(user_id: int, description: str, expected_end_date: date, can_play: bool, notes: str) -> None:
    connection = connect_database()
    cursor = connection.cursor()

    sql = """
        INSERT into injury
        (user_id, description, start_date, expected_end_date, is_current, notes, injury_weighting, can_play)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (user_id, description, date.today(), expected_end_date, True, notes, None, can_play)
    
    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()
    
    
#Function to get player details for one squad - requires user_id
def get_players_in_one_squad(user_id: int) -> list[dict]:
    connection = connect_database()
    cursor = connection.cursor()

    sql = """
        SELECT u.user_id, u.first_name, u.surname, COUNT(mp.match_id) AS games_played, SUM(m.did_win) AS wins
        FROM squad_players sp
        JOIN user u ON u.user_id = sp.user_id
        LEFT JOIN match_players mp ON mp.user_id = u.user_id
        LEFT JOIN `match` m ON m.match_id = mp.match_id
        WHERE sp.squad_id = (SELECT squad_id FROM squad_players WHERE user_id = %s LIMIT 1)
        GROUP BY u.user_id, u.first_name, u.surname
    """
    
    value = (user_id,)
    
    cursor.execute(sql, value)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    
    players = []
    for row in results:
        games_played = row[3]
        wins = row[4] if row[4] is not None else 0
        win_loss_percentage = round((wins / games_played) * 100, 1) if games_played > 0 else 0
        
        players.append({
            "user_id": row[0],
            "firstname": row[1],
            "surname": row[2],
            "games_played": games_played,
            "win_percentage": win_loss_percentage
        })
        
    return players