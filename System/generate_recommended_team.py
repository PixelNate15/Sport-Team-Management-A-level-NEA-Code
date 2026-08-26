from System.form_score_calculation import calculate_form_score
from SQL import get_all_available_players, count_partnership_matches

FORM_THRESHOLD = 0.05
PAIRS_PER_TEAM = 2

def generate_recommended_team(fixture_id):
    players = get_all_available_players(fixture_id)
    if players is not None:
        for player in players:
            player["form_score"] = calculate_form_score(player["user_id"])
    else:
        return None

    sorted_players = sorted(players, key=lambda player: (player["form_score"] is not None, player["form_score"]), reverse=True)
    
    return create_pairings(sorted_players, [])
    
    
def create_pairings(remaining_players, recommended_team):
    if len(recommended_team) == PAIRS_PER_TEAM:
        return recommended_team
    
    if len(remaining_players) < 2:
        return recommended_team
    
    player_1 = remaining_players[0]
    close_players = []
    
    for player in remaining_players[1:]:
        if player["form_score"] is None:
            continue
        if player_1["form_score"] is None:
            continue
        
        difference = abs(player_1["form_score"] - player["form_score"])
        if difference <= FORM_THRESHOLD:
            close_players.append(player)
            
    if close_players:
        partner = choose_best_partner(player_1, close_players)
    else:
        partner = remaining_players[1]
    
    recommended_team.append((player_1, partner))
    
    
    new_remaining_players = []
    for player in remaining_players:
        if (player["user_id"] != player_1["user_id"]) and (player["user_id"] != partner["user_id"]):
            new_remaining_players.append(player)
            
    return create_pairings(new_remaining_players, recommended_team)
            
def choose_best_partner(player, possible_partners):
    best_partner = None
    most_matches_played = -1
    
    for partner in possible_partners:
        matches_played = count_partnership_matches(player["user_id"], partner["user_id"])
        if matches_played > most_matches_played:
            most_matches_played = matches_played
            best_partner = partner
            
    return best_partner