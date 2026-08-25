from SQL import get_match_history_last_three_years, count_fixtures_before_date
from datetime import date

#Constants
HALF_LIFE_DAYS = 60
MIN_OPPONENT_FACTOR = 0.8
DEFAULT_PARTNER_FACTOR = 1


def calculate_form_score(user_id, before_date = None):
    if before_date is None:
        before_date = date.today()
    matches = get_match_history_last_three_years(user_id, before_date)
    
    if not matches:
        return None
    
    weighted_score_total = 0.0
    weight_total = 0.0
    
    for match in matches:
        games_ratio = calculate_games_ratio(match["games_won"], match["games_lost"])
        opponent_factor = calculate_opponent_factor(match)
        partner_factor = calculate_partner_factor(match["partner_form_at_match"])
        recency_factor = calculate_recency_factor(before_date, match["date"])
        
        match_score = games_ratio * opponent_factor * partner_factor
        weighted_score_total += match_score * recency_factor
        weight_total += recency_factor
        
    if weight_total == 0:
        return None
    else:
        return weighted_score_total / weight_total
        

def calculate_games_ratio(games_won, games_lost):
    total_games = games_won + games_lost
    if total_games == 0:
        return 0.0
    return games_won / total_games


def calculate_opponent_factor(match):
    matches_played = count_fixtures_before_date(match["season_id"], match["date"])
    if matches_played >= 2:
        total_teams = match["division_team_count"]
        opponent_league_position = match["opponent_league_position"]
        if total_teams is not None and opponent_league_position is not None:
            weighting_change = (total_teams - opponent_league_position) / 10
            weighting = MIN_OPPONENT_FACTOR + weighting_change
            return weighting
        else:
            return 1.0
    else:
        return 1.0
    

def calculate_partner_factor(partner_form_at_time_of_match):
    if partner_form_at_time_of_match is not None:
        return partner_form_at_time_of_match
    else:
        return DEFAULT_PARTNER_FACTOR
    

def calculate_recency_factor(before_date, match_date):
    days_since_match = (before_date - match_date).days
    return 0.5 ** (days_since_match / HALF_LIFE_DAYS)