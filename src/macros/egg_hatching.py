import src.gamepad as gamepad
from src.log import write_log, LOG_FILE
from src.macros.egg_hatch.oras import main as oras_main

# Eggs Hatched Text File
HATCHED_FILE = "hatched.txt"

# Control Screenshot
CONTROL_SS = "control.png"

# Hatched Screenshot
HATCHED_SS = "hatched.png"

def main(game, method):
    # Loops
    mains = {"oras": oras_main}

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Running 'Egg Hatching' Macro ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    # Supported game
    if game in mains:
        write_log(f"Starting for game '{game}' ...")
    else:  # Any Other Game
        raise NotImplementedError(f"Game '{game}' is unsupported!")

    # Run game script
    mains[game](gp)