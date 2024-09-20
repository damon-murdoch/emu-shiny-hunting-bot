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


def static_encounter_bot(window):

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
    # Updated each revision
    version = "0.1.0"

    # Reset times
    fastest = None
    encounters = 0

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting static encounter bot v{version} ...")

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


def usum_breeding_bot(window):

    # Start at Day Care Entrance

    def deposit(gp, index=1):

        def move(gp, index=1):

            # Box is full
            if index % 30 == 1:
                # Move to next box
                gamepad.press_and_release(
                    gp, [button.XUSB_GAMEPAD_RIGHT_SHOULDER], MENU_PRESS
                )
                time.sleep(1)

            # Remove box from index
            index = index % 30

            while index > 6:
                # Move to next row
                gamepad.press_and_release(
                    gp, [button.XUSB_GAMEPAD_DPAD_DOWN], MENU_PRESS
                )
                index -= 6
                time.sleep(1)

            while index > 1:
                # Move to next index
                gamepad.press_and_release(
                    gp, [button.XUSB_GAMEPAD_DPAD_RIGHT], MENU_PRESS
                )
                index -= 1
                time.sleep(1)

            # Drop Pokemon
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B], MENU_PRESS)

        def select(gp):

            # Select Pokemon
            gamepad.press_and_release_sequence(
                gp,
                [
                    [button.XUSB_GAMEPAD_BACK],  # Switch to 'Move'
                    [button.XUSB_GAMEPAD_DPAD_LEFT],  # Move to Party
                    [button.XUSB_GAMEPAD_B],  # Select Pokemon
                    [button.XUSB_GAMEPAD_DPAD_RIGHT],  # Move to Box
                ],
                1,
            )

        select(gp)
        move(gp, index)

    def spin(gp):
        gp.press_button(button=button.XUSB_GAMEPAD_A)  # Hold Sprint
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["up"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["neutral"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["down"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["down"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["left"], joystick["down"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["left"], joystick["neutral"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["left"], joystick["up"], 0.5)
        gp.release_button(button=button.XUSB_GAMEPAD_A)  # Release Sprint

    def input_loop(gp, index=1, max_spins=20):

        write_log(f"Starting on hatching egg {index} ...")

        # Move to Day Care Lady
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["down"], 0.8)

        # Day Care Lady Menu
        for i in range(10):
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B], 1)
            time.sleep(1)

        # Menu Escape Fallback
        for i in range(2):
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_A], 1)
            time.sleep(1)

        # Walk to Closed Spot
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["down"], 1)
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["down"], 0.8)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["down"], 1)

        # Get on Tauros
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP])

        # Encounter start time
        start = datetime.now()

        # Count spins
        spin_counter = 0
        # Wait for black colour
        while spin_counter < max_spins and screenshot.check_for_colour(window) == False:
            # Spin twice
            for i in range(2):
                spin(gp)
            # Check for egg
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B])
            # Increase spin counter
            spin_counter += 1

        # Encounter end time
        end = datetime.now()

        # Get total duration, seconds
        spin_duration = end - start
        spin_seconds = spin_duration.total_seconds()

        write_log(
            f"Egg {index} hatching cycle completed after {spin_counter} loops ({spin_seconds}s)."
        )

        # Egg hatched (egg menu)
        if spin_counter < max_spins:
            # Wait to reach nickname menu
            screenshot.wait_for_change(window)

            # Wait 1 second
            time.sleep(1)

            # Exit Menu
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_A])

            # Wait for return to game
            screenshot.wait_for_colour(window)
            screenshot.wait_for_change(window)

        # Wait 1 second
        time.sleep(1)

        # Move to top of closed spot
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 1)

        # Get Off Tauros
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP])

        # Wait 1 second
        time.sleep(1)

        # Walk back to the Day Care and enter
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 0.5)
        gamepad.left_stick_and_release(gp, joystick["left"], joystick["up"], 1.4)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 0.9)
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B])

        # Wait 1 second
        time.sleep(1)

        # Move to box and open box menu
        gamepad.left_stick_and_release(gp, joystick["right"], joystick["up"], 1.2)
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B])

        # Wait for menu to load
        screenshot.wait_for_colour(window)
        screenshot.wait_for_change(window)

        # Deposit the new Pokemon
        deposit(gp, index)

        # Wait 1 second
        time.sleep(1)

        # Exit the menu
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_A])

        # Wait to return to game
        screenshot.wait_for_colour(window)
        screenshot.wait_for_change(window)

        # Return to outside
        gamepad.left_stick_and_release(gp, joystick["left"], joystick["down"], 1.2)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["down"], 0.5)

        # Wait 2 seconds
        time.sleep(2)

    # Bot Version
    version = "0.1.0"

    # Hatched Eggs
    hatched = 0

    # Limit of eggs to hatch
    limit = None

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting usum breeding bot v{version} ...")

    # Create the hatch counter file, if empty
    if not os.path.exists(HATCHED_FILE):
        with open(HATCHED_FILE, "w") as file:
            file.write("0")

    # Parse the number of encounters from the file
    with open(HATCHED_FILE, "r") as file:
        hatched = int(file.read())

    write_log(f"Current eggs hatched: {hatched} ...")

    print("Please ensure the game is saved directly outside the door of the Pokemon Nursery.")
    print("For an easy way to do this, enter and exit the Nursery and then save the game.")
    input("Once the game has been saved, press enter to continue.")

    try:
        limit = int(input("Please enter the limit for the number of eggs hatched: "))
        write_log(
            f"Limit provided: {limit}, {(limit - hatched)} more eggs will be hatched."
        )
    except:
        write_log("No limit provided. Eggs will be hatched infinitely.")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    # Restart the game
    gamepad.soft_reset(gp)

    # While no limit, or limit not reached
    while limit == None or hatched < limit:

        try:
            # Encounter start time
            start = datetime.now()

            # Increment hatch counter
            hatched += 1

            # Complete hatch loop
            input_loop(gp, hatched)

            # Save the game
            gamepad.save_game(gp)

            # Encounter end time
            end = datetime.now()

            # Get total duration, seconds
            total_duration = end - start
            total_seconds = total_duration.total_seconds()

            write_log(f"Egg {hatched} completed after {total_seconds}s).")

        except Exception as e:
            write_log(f"Egg hatching failed: {e}")
            return hatched
        try:
            # Update hatch counter
            with open(HATCHED_FILE, "w") as file:
                file.write(str(hatched))
        except Exception as e:  # Failure
            write_log(f"Failed to update hatches: {e}")

        # Wait 2 seconds
        time.sleep(2)

    # Return eggs hatched
    return hatched
