import os, time
from datetime import datetime

import src.screenshot as screenshot
import src.gamepad as gamepad
from vgamepad import XUSB_BUTTON as button

from src.gamepad import JOYSTICK_COORDINATES as joystick

# ~4s input delay
INPUT_DELAY = 4

# ~1.1s delay for shinies
SHINY_DELAY = 1.1

# Encounters Text FIle
ENCOUNTERS_FILE = "encounters.txt"


def static_encounter_bot(window):

    def input_loop(gp):

        # Note: Controller 'B' press maps to 'A' ingame

        gamepad.press_and_release_sequence(
            gp,
            [
                [button.XUSB_GAMEPAD_B],  # Intro Cutscene
                [button.XUSB_GAMEPAD_B],  # Load Save
                [button.XUSB_GAMEPAD_B],  # Start encounter (Normal method)
            ],
            INPUT_DELAY,
        )

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

    # Reset times
    fastest = None
    encounters = 0

    # Create the encounters file, if empty
    if not os.path.exists(ENCOUNTERS_FILE):
        with open(ENCOUNTERS_FILE, "w") as file:
            file.write("0")

    # Parse the number of encounters from the file
    with open(ENCOUNTERS_FILE, "r") as file:
        encounters = int(file.read())

    print(f"Current encounters: {encounters} ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()
    gamepad.configure_citra(gp)

    # Start loop
    while True:

        # Encounter start time
        start = datetime.now()

        try:

            # Increment counter
            encounters += 1

            # Reset game
            gamepad.soft_reset(gp)

            # Perform input loop
            seconds = input_loop(gp)

            # First encounter
            if fastest == None:

                print(f"First encounter took {seconds}s.")

                # Add to duration, resets
                fastest = seconds

                input("Press enter to continue, or ctrl + c to quit:")

            # Current seconds faster than fastest time WITH shiny delay
            elif seconds + SHINY_DELAY < fastest:
                raise Exception("Encounter was too quick!")

            # Update fastest time
            elif fastest > seconds:

                print(f"Fastest encounter updated: {seconds}s.")

                fastest = seconds

            # Current seconds exceeds the shiny delay
            elif seconds > fastest + SHINY_DELAY:

                print("Warning: Potential shiny detected!")

                # Keep going if the user types 'RESET', otherwise return the number of encounters
                if (
                    input(
                        "Type 'RESET' to continue (false positive), or press enter to exit: "
                    )
                    != "RESET"
                ):
                    return encounters

        except Exception as e:  # Failure

            print(f"Encounter failed: {e}, resetting ...")

        try:
            # Parse the number of encounters from the file
            with open(ENCOUNTERS_FILE, "w") as file:
                file.write(str(encounters))
        except Exception as e:  # Failure
            print(f"Failed to update encounters: {e}")

        # Encounter end time
        end = datetime.now()

        # Get total duration, seconds
        total_duration = end - start
        total_seconds = total_duration.total_seconds()

        print(f"Encounter {encounters} completed in {total_seconds}s.")