import subprocess

def run_script(script_name):
    """Run a given Python script using subprocess."""
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully ran {script_name}")
    else:
        print(f"Error running {script_name}: {result.stderr}")
    print(result.stdout)

if __name__ == "__main__":
    # Update the game logs first
    run_script('/scripts/fetch.py')  

    # Now update the databases
    run_script('/scripts/game_log.py')
    run_script('/scripts/team_performance.py')
    run_script('/scripts/player_performance.py')
    run_script('/scripts/update_excel.py')

    print("All scripts have been executed.")
