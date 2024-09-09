import csv
import json
from datetime import datetime
import re
import os

def is_number(s):
    """Check if a string can be converted to a float."""
    try:
        float(s)
        return True
    except ValueError:
        return False

# Load the game logs
with open('game_logs.json', 'r') as file:
    all_games_data = json.load(file)

def clean_player_name(name):
    # Remove any prefix like "a-" or "b-" if present and remove the fielding position
    return re.sub(r'^(a-|b-)?([^\,]+).*', r'\2', name).strip()

cumulative_stats_roah = {}
cumulative_stats_lang = {}

# Iterate over each game and player stats
for game in all_games_data:
    for team_data in game["game"][2][1]:  # Assuming the box score is at index 2
        team_id = team_data["team_id"]
        player_team = "Roah" if team_id == "2404943" else "Lang"
        year = datetime.strptime(game["game"][0][1]["created_at"], "%m/%d/%Y %H:%M:%S").year

        for player_stat in team_data[team_id]["batting_stats"]:
            player_name = clean_player_name(player_stat["player_name"])
            player_key = f"{player_name}_{player_team}_{year}"

            # Initialize player stats if not already present
            if player_team == "Roah":
                if player_key not in cumulative_stats_roah:
                    cumulative_stats_roah[player_key] = {"year": year, "team": player_team, "name": player_name, "PA": 0}
                target_stats = cumulative_stats_roah
            else:
                if player_key not in cumulative_stats_lang:
                    cumulative_stats_lang[player_key] = {"year": year, "team": player_team, "name": player_name, "PA": 0}
                target_stats = cumulative_stats_lang

            # Process and aggregate stats
            for stat_key in ["ab", "h", "doubles", "triples", "hr", "rbi", "bb", "so", "hbp", "sf"]:
                if stat_key in player_stat and is_number(player_stat[stat_key]):
                    if stat_key not in target_stats[player_key]:
                        target_stats[player_key][stat_key] = 0
                    target_stats[player_key][stat_key] += int(player_stat[stat_key])
                # Adjust Plate Appearances
                if stat_key in ["ab", "bb", "hbp", "sf"]:
                    target_stats[player_key]["PA"] += int(player_stat[stat_key])

# Add a function to calculate rate stats and add them to each player's dictionary
def calculate_rate_stats(player_stats):
    for stats in player_stats.values():
        pa = stats["PA"]
        ab = stats.get("ab", 0)
        h = stats.get("h", 0)
        bb = stats.get("bb", 0)
        hbp = stats.get("hbp", 0)
        sf = stats.get("sf", 0)
        doubles = stats.get("doubles", 0)
        triples = stats.get("triples", 0)
        hr = stats.get("hr", 0)
        singles = h - (doubles + triples + hr)


        # Calculate batting average, on-base percentage, and slugging percentage
        stats["BA"] = round(h / ab, 3) if ab else 0
        stats["OBP"] = round((h + bb + hbp) / (ab + bb + hbp + sf), 3) if (ab + bb + hbp + sf) else 0
        stats["SLG"] = round((singles + 2 * doubles + 3 * triples + 4 * hr) / ab, 3) if ab else 0
        stats["OPS"] = round(stats["OBP"] + stats["SLG"], 3)

# Call function to calculate rate stats
calculate_rate_stats(cumulative_stats_roah)
calculate_rate_stats(cumulative_stats_lang)

# Function to write to CSV, adjusted for new logic
def write_stats_to_csv(stats_dict, filename, name):
    if not stats_dict:
        print(f"No data to write for {filename}.")
        return

    # Determine fieldnames from keys in the first item in stats_dict
    fieldnames = list(next(iter(stats_dict.values())).keys())


    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for stats in stats_dict.values():
            writer.writerow(stats)
            
    print(f"player_performance_{name}.csv file has been saved to {filename}")


# Write to CSV files
write_stats_to_csv(cumulative_stats_roah, './data/player_performance_roah.csv', "roah")
write_stats_to_csv(cumulative_stats_lang, './data/player_performance_lang.csv', "lang")
