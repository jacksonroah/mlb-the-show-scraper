import requests
import time
import json

# Constants
USERNAME = "JackTheSon1"
OPPONENT = "Langdog70 ^b54^"
PLATFORM = "psn"
MODE = "arena"
MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds
GAMES_URL = f"https://mlb24.theshow.com/apis/game_history.json?page=1&username={USERNAME}&platform={PLATFORM}&mode={MODE}"

# Load existing game IDs to avoid refetching
existing_game_ids = set()
try:
    with open('game_logs.json', 'r') as file:
        existing_game_logs = json.load(file)
        for game_log in existing_game_logs:
            try:
                game_id = game_log["game"][0][1]["id"]
                existing_game_ids.add(game_id)
            except (KeyError, IndexError):
                print("Warning: A game log entry was missing an expected 'id'. It was skipped.")
except (FileNotFoundError, json.JSONDecodeError):
    existing_game_logs = []

print("Existing Game IDs:", existing_game_ids)  # Log existing IDs

def fetch_games_vs_opponent(url, opponent):
    for attempt in range(MAX_RETRIES):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [game for game in data.get('game_history', []) if opponent in (game.get('home_name'), game.get('away_name'))]
        else:
            print(f"Attempt {attempt + 1}: Error fetching data, status code {response.status_code}")
            time.sleep(RETRY_DELAY)
    return []

def fetch_game_log(game_id):
    url = f"https://mlb24.theshow.com/apis/game_log.json?id={game_id}"
    print(f"Fetching game log from URL: {url}")  # Debugging: Log the URL being fetched
    response = requests.get(url)
    if response.status_code == 200:
        game_log = response.json()
        if "error" not in game_log:  # Check for an "error" key in the response
            return game_log
        else:
            print(f"Error in game log response for Game ID {game_id}: {game_log['error']}")
    else:
        print(f"Failed to fetch game log for Game ID {game_id}: {response.status_code}, Response: {response.text}")
    return None

def update_game_logs(new_game_logs):
    # This function now updates both the game logs and the existing game IDs set
    global existing_game_ids  # Make sure to use the global variable
    for game_log in new_game_logs:
        try:
            game_id = game_log["game"][0][1]["id"]
            existing_game_ids.add(game_id)  # Update the set with new game IDs
        except (KeyError, IndexError):
            print("Warning: A new game log entry was missing an expected 'id'. It was skipped.")

    with open('game_logs.json', 'w') as file:
        json.dump(existing_game_logs + new_game_logs, file, indent=4)


if __name__ == "__main__":
    new_game_logs = []
    filtered_games = fetch_games_vs_opponent(GAMES_URL, OPPONENT)

    for game in filtered_games:
        game_id = game['id']
        if game_id not in existing_game_ids:
            print(f"Fetching new game: Game ID {game_id}")
            game_log = fetch_game_log(game_id)
            if game_log and "error" not in game_log:
                new_game_logs.append(game_log)
                existing_game_ids.add(game_id)  # Update the set with the new game ID
                print(f"Successfully fetched and added Game ID: {game_id}")
            else:
                print(f"Failed to fetch Game ID {game_id} or it returned an error.")
            time.sleep(RETRY_DELAY)
        else:
            print(f"Game ID {game_id} is considered already in the database.")

    if new_game_logs:
        update_game_logs(new_game_logs)
        print(f"Successfully updated game logs with {len(new_game_logs)} new games.")
    else:
        print("No new games to add.")