import os, time, random
from datetime import datetime

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.window as window

from vgamepad import XUSB_BUTTON as button

from src.gamepad import JOYSTICK_COORDINATES as joystick
from src.log import write_log, LOG_FILE

# Menu Button Press
MENU_PRESS = 0.1

# ~1.1s delay for shinies
SHINY_DELAY = 1.1

# Encounters Text File
ENCOUNTERS_FILE = "encounters.txt"

# Eggs Hatched Text File
HATCHED_FILE = "hatched.txt"

# Control Screenshot
CONTROL_SS = "control.png"

# Hatched Screenshot
HATCHED_SS = "hatched.png"


def egg_hatching_bot(citra, game=None, autostart=None):

    def sprint_and_spin(gp):
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

    def input_loop(gp, count=0, max_spins=20):

        # Similarity to control
        similarity = 1.0  # 100%

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

        # Count spins
        spin_counter = 0

        # Wait for black colour
        while spin_counter < max_spins and screenshot.check_for_colour(citra) == False:

            # Spin twice
            for i in range(2):
                sprint_and_spin(gp)

            # Check for egg
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_B])

            # Increase spin counter
            spin_counter += 1

        # Egg hatched (egg menu)
        if spin_counter < max_spins:

            # Wait to reach nickname menu
            screenshot.wait_for_change(citra)

            # Wait 1 second
            time.sleep(1)

            # Control not saved
            if control == False:
                # Save screenshot as 'control.png'
                screenshot.save_screenshot(citra, CONTROL_SS)

                print(f"Control screenshot saved as {CONTROL_SS}.")
            else:
                # Save screenshot as 'hatched.png'
                screenshot.save_screenshot(citra, HATCHED_SS)

                print(f"Encounter screenshot saved as {HATCHED_SS}.")

                print(f"Comparing {HATCHED_SS} to {CONTROL_SS} ...")
                similarity = screenshot.compare_images(
                    HATCHED_SS, CONTROL_SS, debug=True
                )
                print(f"Comparison complete. Reference images saved.")

        # Wait 1 second
        return similarity

    # Bot Version
    version = "1.0.0"

    # Hatched times
    control = False
    hatched = 0

    # Similarities
    similarities = {}

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting Static Encounter Bot v{version} ...")

    # Only implemented for USUM
    if game != "usum":
        raise NotImplementedError("Games other than USUM have not been implemented!")

    # Create the hatched file, if empty
    if not os.path.exists(HATCHED_FILE):
        with open(HATCHED_FILE, "w") as file:
            file.write("0")

    # Parse the number of encounters from the file
    with open(HATCHED_FILE, "r") as file:
        hatched = int(file.read())

    write_log(f"Current hatches: {hatched} ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    # Start loop
    while True:

        # Hatch start time
        start = datetime.now()

        try:
            # Increment counter
            hatched += 1

            write_log(f"Hatching egg {hatched} ...")

            # Random ~0-4s delay
            offset = random.uniform(0.0, 4.0)

            # Reset game (With random delay)
            gamepad.soft_reset(gp, offset=offset)

            # Perform input loop
            similarity = input_loop(gp, control)

            # Similarity as a percentage
            percentage = similarity*100

            # Round to newest whole number
            rounded = str(round(percentage))

            # Control screenshot saved
            control = True

            write_log(f"Similarity to Control: {percentage}%, Rounded: {rounded}%")

            # Rounded not in similarity keys
            if rounded not in similarities:
                # Insert real value into array index
                similarities[rounded] = [similarity]
                input(f"Unseen Rounded Similarity (Potential Shiny): Press enter to continue ...")
            else:  # Already in keys

                # Get the average value in the similarities array
                average = sum(similarities[rounded]) / len(similarities[rounded])

                # Get min/max between sim/avg
                minv = min(similarity, average)
                maxv = max(similarity, average)

                # Get the percentage diff
                avg_similarity = (minv / maxv) * 100

                # [DEBUG] Less than 99.9% Similarity
                if avg_similarity < 99.9:
                    print(f"Avg. Similarity {avg_similarity}% (Potential Shiny) Found: Press enter to continue ...")
                    input("")
                else:
                    print(f"New frame {avg_similarity}% similar to previous matching frames ...")

                # Insert into array index
                similarities[rounded].append(similarity)

        except Exception as e:
            write_log(f"Egg hatching failed: {e}")
            return hatched

        try:
            # Update hatch counter
            with open(HATCHED_FILE, "w") as file:
                file.write(str(hatched))
        except Exception as e:  # Failure
            write_log(f"Failed to update hatches: {e}")

        # Encounter end time
        end = datetime.now()

        # Get total duration, seconds
        total_duration = end - start
        total_seconds = total_duration.total_seconds()

        write_log(f"Egg {hatched} completed after {total_seconds}s.")

        # Reset the game
        gamepad.soft_reset(gp)


def soft_reset_bot(citra, game=None, autostart=None):

    def input_loop(gp):

        # Move control stick forward (For ultra space encounters, etc.)
        gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 1)

        # Wait for fade to black / dark blue
        screenshot.wait_for_colour(citra)
        screenshot.wait_for_change(citra)

        # Time until battle menu
        start = datetime.now()
        screenshot.wait_for_change(citra)
        end = datetime.now()

        # Save screenshot of the last encounter
        screenshot.save_screenshot(citra, "lastencounter.png")

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
                input("First encounter: Press enter to continue ...")
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

            # Error msg string
            errmsg = str(e)

            # Window has crashed
            if errmsg.startswith(
                "Error code from Windows: 1400 - Invalid window handle."
            ):

                # Error Message
                message = "Encounter failed: Window has crashed."

                # Autostart Enabled
                if autostart:
                    write_log(f"{message} Restarting ...")
                    citra = window.start_window(autostart)
                else:  # Cannot Restart
                    raise Exception(message)
            else:  # Generic error
                write_log(f"Encounter failed: {e} Resetting ...")

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
