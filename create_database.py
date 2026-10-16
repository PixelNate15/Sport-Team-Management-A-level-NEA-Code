import mysql.connector


#Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()


#Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS tennis_team_selection")
cursor.execute("USE tennis_team_selection")


#Create User Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    is_captain TINYINT(1) NOT NULL,
    email VARCHAR(100) NOT NULL,
    is_active TINYINT(1) NOT NULL
)
""")


#Create Fixture Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fixture (
    fixture_id INT AUTO_INCREMENT PRIMARY KEY,
    created_by_id INT NOT NULL,
    opponent_name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    location VARCHAR(20) NOT NULL,
    is_home TINYINT(1) NOT NULL,
    division INT NOT NULL,
    notes TEXT,

    FOREIGN KEY (created_by_id)
    REFERENCES user(user_id)
)
""")


#Create Availability Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS availability (
    availability_id INT AUTO_INCREMENT PRIMARY KEY,
    fixture_id INT NOT NULL,
    user_id INT NOT NULL,
    is_available TINYINT(1) NOT NULL,
    reason TEXT,
    date_submitted DATE NOT NULL,

    FOREIGN KEY (fixture_id)
    REFERENCES fixture(fixture_id),

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


#Create Form Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS form (
    form_score_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date_calculated DATE NOT NULL,
    recent_win_rate FLOAT NOT NULL,
    old_win_rate FLOAT NOT NULL,
    recency_weighting FLOAT NOT NULL,
    final_score INT NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


#Create Injury Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS injury (
    injury_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    expected_end_date DATE NOT NULL,
    is_current TINYINT(1) NOT NULL,
    notes TEXT NOT NULL,
    injury_weighting FLOAT NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


#Create Match Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `match` (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    fixture_id INT NOT NULL,
    pair_number INT NOT NULL,
    opponent_pair_number INT NOT NULL,
    date DATE NOT NULL,
    did_win TINYINT(1) NOT NULL,
    sets_won INT NOT NULL,
    sets_lost INT NOT NULL,
    games_won INT NOT NULL,
    games_lost INT NOT NULL,
    opponent_weighting FLOAT NOT NULL,

    FOREIGN KEY (fixture_id)
    REFERENCES fixture(fixture_id)
)
""")


#Create Match Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS match_player (
    match_player_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    user_id INT NOT NULL,
    partner_user_id INT NOT NULL,
    player_weighting FLOAT NOT NULL,

    FOREIGN KEY (match_id)
    REFERENCES `match`(match_id),

    FOREIGN KEY (user_id)
    REFERENCES user(user_id),

    FOREIGN KEY (partner_user_id)
    REFERENCES user(user_id)
)
""")


#Create Feedback Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    reviewed_id INT NOT NULL,
    overall_rating INT NOT NULL,
    key_moments_rating INT NOT NULL,
    communication_rating INT NOT NULL,
    comments TEXT,
    date DATE NOT NULL,

    FOREIGN KEY (match_id)
    REFERENCES `match`(match_id),

    FOREIGN KEY (reviewer_id)
    REFERENCES user(user_id),

    FOREIGN KEY (reviewed_id)
    REFERENCES user(user_id)
)
""")


#Create Settings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    theme TINYINT(1) NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


#Create Squad Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS squad (
    squad_id INT AUTO_INCREMENT PRIMARY KEY,
    squad_name VARCHAR(50) NOT NULL
)
""")


#Create Squad PLayers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS squad_players (
    squad_player_id INT AUTO_INCREMENT PRIMARY KEY,
    squad_id INT NOT NULL,
    user_id INT NOT NULL,

    FOREIGN KEY (squad_id)
    REFERENCES squad(squad_id),

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


#Create Team Selection Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS team_selection (
    team_selection_id INT AUTO_INCREMENT PRIMARY KEY,
    fixture_id INT NOT NULL,
    date DATE NOT NULL,
    is_suggested_by_system TINYINT(1) NOT NULL,
    notes TEXT NOT NULL,

    FOREIGN KEY (fixture_id)
    REFERENCES fixture(fixture_id)
)
""")


#Create Team Selection Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS team_selection_players (
    team_selection_player_id INT AUTO_INCREMENT PRIMARY KEY,
    team_selection_id INT NOT NULL,
    user_id INT NOT NULL,
    pair_number INT NOT NULL,
    selection_order INT NOT NULL,
    was_suggested TINYINT(1) NOT NULL,
    reason_for_overwriting TEXT,

    FOREIGN KEY (team_selection_id)
    REFERENCES team_selection(team_selection_id),

    FOREIGN KEY (user_id)
    REFERENCES user(user_id)
)
""")


connection.commit()
cursor.close()
connection.close()