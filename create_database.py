import mysql.connector


#Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()


#Delete Old Database
cursor.execute("DROP DATABASE IF EXISTS tennis_team_selection")


#Create Database
cursor.execute("CREATE DATABASE tennis_team_selection")
cursor.execute("USE tennis_team_selection")


#Create Club Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `club` (
  `club_id` int(11) NOT NULL AUTO_INCREMENT,
  `club_name` varchar(100) NOT NULL,
  PRIMARY KEY (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Division Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `division` (
  `division_id` int(11) NOT NULL AUTO_INCREMENT,
  `division_name` varchar(50) NOT NULL,
  `team_count` int(11) NOT NULL,
  PRIMARY KEY (`division_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Season Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `season` (
  `season_id` int(11) NOT NULL AUTO_INCREMENT,
  `season_name` varchar(50) NOT NULL,
  `is_current` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`season_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create User Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `is_captain` tinyint(1) NOT NULL,
  `email` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `club_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_users_club` (`club_id`),
  CONSTRAINT `fk_users_club` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Squad Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `squad` (
  `squad_id` int(11) NOT NULL AUTO_INCREMENT,
  `squad_name` varchar(50) NOT NULL,
  `squad_ranking` int(11) DEFAULT NULL,
  `club_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`squad_id`),
  KEY `fk_squad_club` (`club_id`),
  KEY `fk_squad_division` (`division_id`),
  CONSTRAINT `fk_squad_club` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_squad_division` FOREIGN KEY (`division_id`) REFERENCES `division` (`division_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Squad Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `squad_players` (
  `squad_player_id` int(11) NOT NULL AUTO_INCREMENT,
  `squad_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`squad_player_id`),
  KEY `squad_id` (`squad_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `squad_players_ibfk_1` FOREIGN KEY (`squad_id`) REFERENCES `squad` (`squad_id`) ON UPDATE CASCADE,
  CONSTRAINT `squad_players_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Fixture Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `fixture` (
  `fixture_id` int(11) NOT NULL AUTO_INCREMENT,
  `created_by_id` int(11) NOT NULL,
  `opponent_name` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `location` varchar(20) NOT NULL,
  `is_home` tinyint(1) NOT NULL,
  `division` int(11) NOT NULL,
  `opponent_league_position` int(11) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `squad_id` int(11) NOT NULL,
  `season_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`fixture_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `squad_id` (`squad_id`),
  KEY `fixture_season_fk` (`season_id`),
  CONSTRAINT `fixture_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE,
  CONSTRAINT `fixture_ibfk_2` FOREIGN KEY (`squad_id`) REFERENCES `squad` (`squad_id`),
  CONSTRAINT `fixture_season_fk` FOREIGN KEY (`season_id`) REFERENCES `season` (`season_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Availability Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `availability` (
  `availability_id` int(11) NOT NULL AUTO_INCREMENT,
  `fixture_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `reason` text DEFAULT NULL,
  `date_submitted` date NOT NULL,
  PRIMARY KEY (`availability_id`),
  KEY `fixture_id` (`fixture_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `availability_ibfk_1` FOREIGN KEY (`fixture_id`) REFERENCES `fixture` (`fixture_id`) ON UPDATE CASCADE,
  CONSTRAINT `availability_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Injury Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `injury` (
  `injury_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `description` text NOT NULL,
  `start_date` date NOT NULL,
  `expected_end_date` date NOT NULL,
  `is_current` tinyint(1) NOT NULL,
  `notes` text NOT NULL,
  `can_play` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`injury_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `injury_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Match Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `match` (
  `match_id` int(11) NOT NULL AUTO_INCREMENT,
  `fixture_id` int(11) NOT NULL,
  `pair_number` int(11) NOT NULL,
  `opponent_pair_number` int(11) NOT NULL,
  `date` date NOT NULL,
  `did_win` tinyint(1) NOT NULL,
  `sets_won` int(11) NOT NULL,
  `sets_lost` int(11) NOT NULL,
  `games_won` int(11) NOT NULL,
  `games_lost` int(11) NOT NULL,
  PRIMARY KEY (`match_id`),
  KEY `fixture_id` (`fixture_id`),
  CONSTRAINT `match_ibfk_1` FOREIGN KEY (`fixture_id`) REFERENCES `fixture` (`fixture_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Match Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `match_players` (
  `match_player_id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `partner_user_id` int(11) NOT NULL,
  `partner_form_at_match` decimal(6,3) DEFAULT NULL,
  PRIMARY KEY (`match_player_id`),
  KEY `match_id` (`match_id`),
  KEY `user_id` (`user_id`),
  KEY `partner_user_id` (`partner_user_id`),
  CONSTRAINT `match_players_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`match_id`) ON UPDATE CASCADE,
  CONSTRAINT `match_players_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE,
  CONSTRAINT `match_players_ibfk_3` FOREIGN KEY (`partner_user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Partner Feedback Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `partner_feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `reviewer_id` int(11) NOT NULL,
  `reviewed_id` int(11) NOT NULL,
  `overall_rating` int(11) NOT NULL,
  `key_moments_rating` int(11) NOT NULL,
  `communication_rating` int(11) NOT NULL,
  `comments` text DEFAULT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`feedback_id`),
  KEY `match_id` (`match_id`),
  KEY `reviewer_id` (`reviewer_id`),
  KEY `reviewed_id` (`reviewed_id`),
  CONSTRAINT `partner_feedback_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`match_id`) ON UPDATE CASCADE,
  CONSTRAINT `partner_feedback_ibfk_2` FOREIGN KEY (`reviewer_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE,
  CONSTRAINT `partner_feedback_ibfk_3` FOREIGN KEY (`reviewed_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Settings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `settings` (
  `setting_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `theme` tinyint(1) NOT NULL,
  PRIMARY KEY (`setting_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `settings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Team Selection Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `team_selection` (
  `team_selection_id` int(11) NOT NULL AUTO_INCREMENT,
  `fixture_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `is_suggested_by_system` tinyint(1) NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`team_selection_id`),
  KEY `fixture_id` (`fixture_id`),
  CONSTRAINT `team_selection_ibfk_1` FOREIGN KEY (`fixture_id`) REFERENCES `fixture` (`fixture_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

#Create Team Selection Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS `team_selection_players` (
  `team_selection_player_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_selection_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `pair_number` int(11) NOT NULL,
  `selection_order` int(11) NOT NULL,
  `was_suggested` tinyint(1) NOT NULL,
  `reason_for_overwritting` text DEFAULT NULL,
  PRIMARY KEY (`team_selection_player_id`),
  KEY `team_selection_id` (`team_selection_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `team_selection_players_ibfk_1` FOREIGN KEY (`team_selection_id`) REFERENCES `team_selection` (`team_selection_id`) ON UPDATE CASCADE,
  CONSTRAINT `team_selection_players_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")


connection.commit()
cursor.close()
connection.close()