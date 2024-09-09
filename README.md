# MLB The Show 24 Game Analysis Tool

## Overview
This project automates the collection, processing, and analysis of game data from MLB The Show 24, focusing on head-to-head matches between two specific players. It leverages the game's API to fetch data, process it, and generate comprehensive statistics in an Excel spreadsheet.

## Features
- Data retrieval of game statistics from MLB The Show 24's API
- Detailed game log parsing and analysis
- Player performance tracking and statistics calculation
- Team performance analysis including inning-by-inning scoring
- Automated Excel spreadsheet generation with up-to-date statistics

## Project Structure
The project consists of several Python scripts, each handling a specific part of the data pipeline:

1. `fetch.py`: Retrieves game logs from the MLB The Show 24 API.
2. `game_log.py`: Processes raw game logs, extracting key information like stadium, game time, and difficulty settings.
3. `player_performance.py`: Analyzes individual player statistics, calculating cumulative and rate stats.
4. `team_performance.py`: Compiles team-level statistics and inning-by-inning scoring data.
5. `update_excel.py`: Consolidates all processed data into a single Excel workbook.
6. `main_workflow.py`: Orchestrates the execution of all scripts in the correct order.

## Detailed Script Descriptions

### fetch.py
- Pulls game logs from MLB The Show 24's API
- Filters games between specified players
- Stores raw game data in JSON format

### game_log.py
- Extracts detailed information from game logs
- Processes data such as stadium names, game start times, and difficulty settings
- Outputs a CSV file with game-by-game details

### player_performance.py
- Analyzes individual player statistics across all games
- Calculates cumulative stats (hits, runs, etc.) and rate stats (BA, OBP, SLG, OPS)
- Generates separate CSV files for each player's performance

### team_performance.py
- Compiles team-level statistics for each game
- Includes inning-by-inning scoring data
- Outputs a comprehensive CSV file with detailed team performance metrics

### update_excel.py
- Consolidates all CSV files into a single Excel workbook
- Updates or creates new sheets for each data category
- Ensures the final Excel file contains the most up-to-date information

### main_workflow.py
- Coordinates the execution of all scripts in the correct sequence
- Ensures data integrity and proper flow through the analysis pipeline

## Technologies Used
- Python
- Pandas for data manipulation
- Requests library for API interactions
- JSON for data parsing
- openpyxl for Excel file handling

## Future Improvements
- More reliable fetching, MLBTS's API is a bit testy on whether or not Game Logs exist. 
- Automation of updates, fetching on its own every day/hour so you don't have to manually run the script.
