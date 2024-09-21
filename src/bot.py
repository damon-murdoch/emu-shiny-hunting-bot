import math, os, time, random
from datetime import datetime

import src.screenshot as screenshot
import src.gamepad as gamepad
from vgamepad import XUSB_BUTTON as button

from src.gamepad import JOYSTICK_COORDINATES as joystick
from src.log import write_log, LOG_FILE

# Menu Button Press
MENU_PRESS = 0.1

# ~1.1s delay for shinies
SHINY_DELAY = 1.1

# Encounters Text FIle
ENCOUNTERS_FILE = "encounters.txt"

# Eggs Hatched Text File
HATCHED_FILE = "hatched.txt"


def static_encounter_bot(window, game=None):

    def input_loop(gp):

        # Move control stick forward (For ultra space encounters, etc.)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 1)

        # Wait for fade to black / dark blue
        screenshot.wait_for_colour(window)
        screenshot.wait_for_change(window)

        # Time until battle menu
        start = datetime.now()
        screenshot.wait_for_change(window)
        end = datetime.now()

        # Save screenshot of the last encounter
        screenshot.save_screenshot(window, "lastencounter.png")

        # Seconds to load battle menu
        duration = end - start

        # Return seconds
        return duration.total_seconds()

    # Bot Version
    version = "1.0.0"

    # Reset times
    fastest = None
    encounters = 0

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting Static Encounter Bot v{version} ...")

    # Create the encounters file, if empty
    if not os.path.exists(ENCOUNTERS_FILE):
        with open(ENCOUNTERS_FILE, "w") as file:
            file.write("0")

    # Parse the number of encounters from the file
    with open(ENCOUNTERS_FILE, "r") as file:
        encounters = int(file.read())

    write_log(f"Current encounters: {encounters} ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    # Start loop
    while True:

        # Encounter start time
        start = datetime.now()

        try:
            # Increment counter
            encounters += 1

            write_log(f"Starting encounter {encounters} ...")

            # Random ~0-4s delay
            offset = random.uniform(0.0, 4.0)

            # Reset game (With random delay)
            gamepad.soft_reset(gp, offset=offset)

            # Perform input loop
            seconds = input_loop(gp)

            write_log(f"Battle menu loaded in {seconds}s.")

            # First encounter
            if fastest == None:
                input("First encounter: press enter to continue")
                fastest = seconds

            # Update fastest time
            elif fastest > seconds:
                write_log(f"Fastest load time updated.")
                fastest = seconds

            # Encounter is too quick (error)
            elif seconds + SHINY_DELAY < fastest:
                raise Exception("Load time was too quick!")

            # Potential shiny detected
            elif seconds > fastest + SHINY_DELAY:
                write_log(f"Potential shiny detected after {encounters} encounters.")
                return encounters

        except Exception as e:  # Failure
            write_log(f"Encounter failed: {e}, resetting ...")

        try:
            # Parse the number of encounters from the file
            with open(ENCOUNTERS_FILE, "w") as file:
                file.write(str(encounters))
        except Exception as e:  # Failure
            write_log(f"Failed to update encounters: {e}")

        # Encounter end time
        end = datetime.now()

        # Get total duration, seconds
        total_duration = end - start
        total_seconds = total_duration.total_seconds()

        write_log(f"Resetting encounter {encounters} after {total_seconds}s.")
