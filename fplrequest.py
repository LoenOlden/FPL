import requests
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch FPL data: {e}")
        raise

def get_players():
    data = fetch_fpl_data()
    return data.get('elements', [])

def save_player_data_to_csv(players, file_path='players_data.csv'):
    # Define all possible fields you want to include
    fieldnames = [
        'id', 'first_name', 'second_name', 'web_name', 'team', 'position', 'cost', 'total_points',
        'expected_goals', 'expected_assists', 'expected_goal_involvements', 'expected_goals_conceded',
        'minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals',
        'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus',
        'bps', 'influence', 'creativity', 'threat', 'ict_index', 'starts', 'expected_goals_per_90',
        'saves_per_90', 'expected_assists_per_90', 'expected_goal_involvements_per_90',
        'expected_goals_conceded_per_90', 'goals_conceded_per_90', 'now_cost_rank', 'form_rank',
        'points_per_game_rank', 'selected_rank', 'starts_per_90', 'clean_sheets_per_90'
    ]

    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for player in players:
                writer.writerow({
                    'id': player['id'],
                    'first_name': player['first_name'],
                    'second_name': player['second_name'],
                    'web_name': player['web_name'],
                    'team': player['team'],
                    'position': player['element_type'],
                    'cost': player['now_cost'] / 10, 
                    'total_points': player['total_points'],
                    'expected_goals': player.get('expected_goals', 'N/A'),
                    'expected_assists': player.get('expected_assists', 'N/A'),
                    'expected_goal_involvements': player.get('expected_goal_involvements', 'N/A'),
                    'expected_goals_conceded': player.get('expected_goals_conceded', 'N/A'),
                    'minutes': player.get('minutes', 'N/A'),
                    'goals_scored': player.get('goals_scored', 'N/A'),
                    'assists': player.get('assists', 'N/A'),
                    'clean_sheets': player.get('clean_sheets', 'N/A'),
                    'goals_conceded': player.get('goals_conceded', 'N/A'),
                    'own_goals': player.get('own_goals', 'N/A'),
                    'penalties_saved': player.get('penalties_saved', 'N/A'),
                    'penalties_missed': player.get('penalties_missed', 'N/A'),
                    'yellow_cards': player.get('yellow_cards', 'N/A'),
                    'red_cards': player.get('red_cards', 'N/A'),
                    'saves': player.get('saves', 'N/A'),
                    'bonus': player.get('bonus', 'N/A'),
                    'bps': player.get('bps', 'N/A'),
                    'influence': player.get('influence', 'N/A'),
                    'creativity': player.get('creativity', 'N/A'),
                    'threat': player.get('threat', 'N/A'),
                    'ict_index': player.get('ict_index', 'N/A'),
                    'starts': player.get('starts', 'N/A'),
                    'expected_goals_per_90': player.get('expected_goals_per_90', 'N/A'),
                    'saves_per_90': player.get('saves_per_90', 'N/A'),
                    'expected_assists_per_90': player.get('expected_assists_per_90', 'N/A'),
                    'expected_goal_involvements_per_90': player.get('expected_goal_involvements_per_90', 'N/A'),
                    'expected_goals_conceded_per_90': player.get('expected_goals_conceded_per_90', 'N/A'),
                    'goals_conceded_per_90': player.get('goals_conceded_per_90', 'N/A'),
                    'now_cost_rank': player.get('now_cost_rank', 'N/A'),
                    'form_rank': player.get('form_rank', 'N/A'),
                    'points_per_game_rank': player.get('points_per_game_rank', 'N/A'),
                    'selected_rank': player.get('selected_rank', 'N/A'),
                    'starts_per_90': player.get('starts_per_90', 'N/A'),
                    'clean_sheets_per_90': player.get('clean_sheets_per_90', 'N/A'),
                })
        logging.info(f"Data has been saved to {file_path}")
    except IOError as e:
        logging.error(f"Failed to save player data to CSV: {e}")

# Example usage
if __name__ == "__main__":
    try:
        players = get_players()
        save_player_data_to_csv(players)
    except Exception as e:
        logging.error(f"An error occurred: {e}")