import requests
import time
import json  # Import the json module

# Constants for fetching games
USERNAME = "JackTheSon1"
OPPONENT = "Langdog70 ^b54^"
PLATFORM = "psn"
MODE = "arena"
GAMES_URL = f"https://mlb24.theshow.com/apis/game_history.json?page=1&username={USERNAME}&platform={PLATFORM}&mode={MODE}"

def fetch_game_log(game_id):
    url = f"https://mlb24.theshow.com/apis/game_log.json?id={game_id}"
    response = requests.get(url)
    if response.status_code == 200:
        game_log = response.json()
        if "error" in game_log:
            print(f"Game ID {game_id} returned an error in the game log: {game_log['error']}")
            return None
        return game_log
    else:
        print(f"Failed to fetch game log for game ID {game_id}: {response.status_code}, Response: {response.text}")
        return None
    
print(json.dumps(fetch_game_log("238901960"), indent = 4))

# def fetch_games_vs_opponent(url, opponent):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Error fetching data: {response.status_code}")
#         return []
#     data = response.json()
#     return [game for game in data.get('game_history', []) if opponent in (game.get('home_name'), game.get('away_name'))]

# def fetch_game_log(game_id):
#     url = f"https://mlb24.theshow.com/apis/game_log.json?id={game_id}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         game_log = response.json()
#         if "error" in game_log:
#             print(f"Game ID {game_id} returned an error in the game log: {game_log['error']}")
#             return None
#         return game_log
#     else:
#         print(f"Failed to fetch game log for game ID {game_id}: {response.status_code}, Response: {response.text}")
#         return None

# def save_game_logs_to_json(game_logs, filename='game_logs.json'):
#     with open(filename, 'w') as f:
#         json.dump(game_logs, f, indent=4)

# def debug_game_log_availability(game_ids):
#     all_game_logs = []  # Initialize a list to collect all game logs
#     for game_id in game_ids:
#         print(f"\nRequesting game log for Game ID: {game_id}")
#         game_log = fetch_game_log(game_id)
#         if game_log:
#             all_game_logs.append(game_log)  # Collect the game log
#             print(f"Successfully fetched game log for Game ID {game_id}.")
#         else:
#             print(f"Failed to fetch or parse game log for Game ID {game_id}.")
#         time.sleep(5)  # Delay to avoid rate limits
#     return all_game_logs  # Return the collected game logs

# if __name__ == "__main__":
#     filtered_games = fetch_games_vs_opponent(GAMES_URL, OPPONENT)
#     if filtered_games:
#         game_ids = [game['id'] for game in filtered_games]
#         game_logs = debug_game_log_availability(game_ids)  # Fetch and collect game logs
#         save_game_logs_to_json(game_logs)  # Save the game logs to a JSON file
#         print("Game logs have been saved to game_logs.json.")
#     else:
#         print("No games found against the specified opponent or failed to fetch games.")
