import mysql.connector
from SQL.connection import connect_database

#Function to get partner feedback for one fixture - requires fixture_id and user_id
def get_partner_feedback_for_one_fixture(fixture_id: int, user_id: int) -> list[dict]:
    try:
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
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get recent partner feedback for one user - requires user_id
def get_recent_partner_feedback(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT f.opponent_name, f.date, f.is_home, pf.overall_rating, pf.key_moments_rating, pf.communication_rating, pf.comments
        FROM  partner_feedback pf
        JOIN `match` m ON m.match_id = pf.match_id
        JOIN fixture f ON f.fixture_id = m.fixture_id
        WHERE pf.reviewed_id = %s AND f.date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND f.date <= CURDATE()
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
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get see if a user has submitted partner feedback - requires fixture_id and user_id
def has_submitted_feedback(fixture_id: int, user_id: int) -> bool:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        SELECT 1
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
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the name of a partner for a fixture - requires user_id and match_id
def get_partner_info(user_id: int, match_id: int) -> dict:
    try:
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
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to insert partner feedback for a fixture
def insert_partner_feedback(match_id: int, reviewer_id: int, reviewed_id: int, overall_rating: int, key_moments_rating: int, communication_rating: int, comments: str) -> None:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
        INSERT INTO partner_feedback
        (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (match_id, reviewer_id, reviewed_id, overall_rating, key_moments_rating, communication_rating, comments, date.today())

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")


#Function to get the last 10 feedback scores about a user - requires user_id
def get_last_ten_feedback_scores(user_id: int) -> list[dict]:
    try:
        connection = connect_database()
        cursor = connection.cursor()

        sql = """
            SELECT overall_rating, key_moments_rating, communication_rating, date
            FROM partner_feedback pf
            WHERE reviewed_id = %s
            ORDER BY date DESC
            LIMIT 10
        """

        value = (user_id,)

        cursor.execute(sql, value)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        feedback_scores = []
        for row in results:
            feedback_scores.append({
                "overall_rating": row[0],
                "key_moments_rating": row[1],
                "communication_rating": row[2]
            })

        feedback_scores.reverse()

        return feedback_scores
    except ConnectionError:
        print("ERROR: Could not connect to database")

    except mysql.connector.Error as err:
        print(f"ERROR: SQL query failed: {err}")
