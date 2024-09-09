import csv
import json
import os

# Load the game logs from the JSON file
game_logs_path = 'game_logs.json'
with open(game_logs_path, 'r') as file:
    all_games_data = json.load(file)

# Define player IDs for Roah and Lang for identification
player_ids = {"2404943": "Roah", "18053066": "Lang"}

# Initialize a list to store comprehensive game data
comprehensive_game_data = []

for game in all_games_data:
    # Extract general game information
    game_id = game["game"][0][1]["id"]
    game_date = game["game"][0][1]["created_at"]
    home_player_id = game["game"][0][1]["home_player_id"]
    away_player_id = game["game"][0][1]["away_player_id"]
    total_innings = int(game["game"][0][1]["innings"])

    # Process team performance data within the 'box_score' section
    for team_data in game["game"][2][1]:
        team_id = team_data["team_id"]
        team_name = team_data["team_name"]
        batting_stats = team_data[team_id]["batting_totals"]

        player_name = player_ids.get(team_id)
        team_status = "Home" if team_id == home_player_id else "Away"

        total_singles = total_doubles = total_triples = total_home_runs = 0
        for player_stat in team_data[team_id]["batting_stats"]:
            player_doubles = int(player_stat.get("doubles", 0))
            player_triples = int(player_stat.get("triples", 0))
            player_home_runs = int(player_stat["hr"])
            player_hits = int(player_stat["h"])

            player_singles = player_hits - (player_doubles + player_triples + player_home_runs)
            total_singles += player_singles
            total_doubles += player_doubles
            total_triples += player_triples
            total_home_runs += player_home_runs

        total_hits = total_singles + total_doubles + total_triples + total_home_runs
        total_walks = int(batting_stats["bb"])
        total_ab = int(batting_stats["ab"])
        total_hbp = int(batting_stats.get("hbp", 0))
        total_sf = int(batting_stats.get("sf", 0))
        pa = total_ab + total_walks + total_hbp + total_sf

        batting_average = total_hits / total_ab
        obp = (total_hits + total_walks + total_hbp) / pa
        slg = (total_singles + total_doubles * 2 + total_triples * 3 + total_home_runs * 4) / total_ab

        # Initialize the game entry with existing data
        game_entry = {
             "Game ID": game_id,
            "Date": game_date,
            "Player": player_name,
            "Team Status": team_status,
            "Team Name": team_name,
            "At Bats": batting_stats["ab"],
            "Total Hits": batting_stats["h"],
            "Singles": total_singles,
            "Doubles": total_doubles,
            "Triples": total_triples,
            "Home Runs": total_home_runs,
            "RBIs": batting_stats["rbi"],
            "Walks": batting_stats["bb"],
            "Strikeouts": batting_stats["so"],
            "BA": round(batting_average, 3),
            "OBP": round(obp, 3),
            "SLG": round(slg, 3),
            "OPS": round(obp + slg, 3)
        }

        # Add inning-specific runs
        for inning in range(1, 12):
            runs_key = f"{'home' if team_status == 'Home' else 'away'}_runs_{inning}"
            game_entry[f"runs_{inning}"] = game["game"][0][1].get(runs_key, "n/a") if inning <= total_innings else "n/a"

        comprehensive_game_data.append(game_entry)

# Dynamic fieldnames including runs per inning
fieldnames = [
    "Game ID", "Date", "Player", "Team Status", "Team Name", "At Bats", "Total Hits", "Singles", 
    "Doubles", "Triples", "Home Runs", "RBIs", "Walks", "Strikeouts", "BA", "OBP", "SLG", "OPS"
] + [f"runs_{i}" for i in range(1, 12)]

data_folder = './data'

# Ensure the data folder exists
os.makedirs(data_folder, exist_ok=True)

# Define the path to your CSV file within the data folder
csv_file_path = os.path.join(data_folder, 'team_performance.csv')

# Write to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comprehensive_game_data)

print(f"CSV file has been saved to {csv_file_path}")

    