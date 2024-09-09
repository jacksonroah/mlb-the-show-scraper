import csv
import json
import re
from datetime import datetime
import os

def extract_stadium_name(game_log_text):
    # Step 1: Capture up to 50 characters before the elevation pattern
    match = re.search(r'.{0,50}\s+\(\d+ ft elevation\)', game_log_text)
    if not match:
        return "N/A"  # Early return if no match found
    
    text_before_elevation = match.group(0)
    
    # Step 2: Refine the captured text to extract the stadium name
    # Splitting by caret and getting everything after the third caret, if it exists
    parts = text_before_elevation.split('^')
    if len(parts) >= 4:
        refined_text = '^'.join(parts[3:])
        # Further cleaning to remove any remaining unwanted characters or patterns
        stadium_name = re.sub(r'^\^e\^', '', refined_text)  # Remove starting ^e^
        stadium_name = re.sub(r'\s+\(\d+ ft elevation\).*', '', stadium_name)  # Remove elevation info and anything after
        stadium_name = re.sub(r'^n\^', '', stadium_name)  # Remove leading n^ if present

        # New step: Check and remove trailing ^e^ or ^ if present
        stadium_name = re.sub(r'\^e\^$', '', stadium_name)  # Remove trailing ^e^ if present
        stadium_name = re.sub(r'\^$', '', stadium_name)  # Remove trailing ^ if present

        return stadium_name.strip()
    else:
        return "N/A"

def extract_game_log_details(game_log_text):

    stadium = extract_stadium_name(game_log_text)

    # Extracting start time
    start_time_regex = r"Scheduled First Pitch: (.+?)(?:am|pm)"
    start_time_match = re.search(start_time_regex, game_log_text, re.IGNORECASE)
    start_time = start_time_match.group(1).strip() if start_time_match else "N/A"

    # Extracting hitting difficulty
    hitting_difficulty_regex = r"Hitting Difficulty is (.*?)[.](?=\^n\^)"
    hitting_difficulty_match = re.search(hitting_difficulty_regex, game_log_text, re.DOTALL)
    hitting_difficulty = hitting_difficulty_match.group(1) if hitting_difficulty_match else "N/A"

    # Extracting pitching difficulty
    pitching_difficulty_regex = r"Pitching Difficulty is (.*?)[.](?=\^n\^)"
    pitching_difficulty_match = re.search(pitching_difficulty_regex, game_log_text, re.DOTALL)
    pitching_difficulty = pitching_difficulty_match.group(1) if pitching_difficulty_match else "N/A"

    return stadium, start_time, hitting_difficulty, pitching_difficulty

def main():
    with open('game_logs.json', 'r') as file:
        game_data = json.load(file)

    reversed_game_data = list(reversed(game_data))  # Reverse the game order for numbering

    csv_rows = []

    for index, game in enumerate(reversed_game_data, start=1):
        game_details = game["game"][0][1]
        game_log_text = game["game"][1][1]  # Assuming the game log is at this location
        stadium, start_time, hitting_difficulty, pitching_difficulty = extract_game_log_details(game_log_text)

        # Prepare row for CSV
        row = {
            "Game Number": index,
            "Date": datetime.strptime(game_details["created_at"], "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d"),
            "Winner": "Roah" if game_details["winning_mlb_team_id"] == "2404943" else "Lang",
            "Home Team": "Roah" if game_details["home_player_id"] == "2404943" else "Lang",
            "Away Team": "Roah" if game_details["away_player_id"] == "2404943" else "Lang",
            "Roah Team Name": game_details["home_full_name"] if game_details["home_player_id"] == "2404943" else game_details["away_full_name"],
            "Lang Team Name": game_details["home_full_name"] if game_details["home_player_id"] == "18053066" else game_details["away_full_name"],
            "Stadium": stadium,
            "Start Time": start_time,
            "Pitching Difficulty": pitching_difficulty,
            "Hitting Difficulty": hitting_difficulty,
            "Roah Runs": game_details["home_runs"] if game_details["home_player_id"] == "2404943" else game_details["away_runs"],
            "Lang Runs": game_details["home_runs"] if game_details["home_player_id"] == "18053066" else game_details["away_runs"],
            "Roah Hits": game_details["home_hits"] if game_details["home_player_id"] == "2404943" else game_details["away_hits"],
            "Lang Hits": game_details["home_hits"] if game_details["home_player_id"] == "18053066" else game_details["away_hits"],
            "Innings": game_details["innings"]
        }
        csv_rows.append(row)

    data_folder = './data'

    # Ensure the data folder exists
    os.makedirs(data_folder, exist_ok=True)

    # Define the path to your CSV file within the data folder
    csv_file_path = os.path.join(data_folder, 'team_performance.csv')

    # Writing to CSV
    with open('./data/game_log.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = [
            "Game Number", "Date", "Winner", "Home Team", "Away Team", "Roah Team Name", "Lang Team Name",
            "Stadium", "Start Time", "Pitching Difficulty", "Hitting Difficulty",
            "Roah Runs", "Lang Runs", "Roah Hits", "Lang Hits", "Innings"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"gamelog.csv file has been saved to {csv_file_path}")


if __name__ == "__main__":
    main()
