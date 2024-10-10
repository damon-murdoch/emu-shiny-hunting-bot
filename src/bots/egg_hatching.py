import os, time, random
from datetime import datetime

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.window as window

from vgamepad import XUSB_BUTTON as button

from src.gamepad import JOYSTICK_COORDINATES as joystick
from src.gamepad import ABXY_MAP as abxy_map
from src.log import write_log, LOG_FILE

from src.common import handle_exception

# Eggs Hatched Text File
HATCHED_FILE = "hatched.txt"

# Control Screenshot
CONTROL_SS = "control.png"

# Hatched Screenshot
HATCHED_SS = "hatched.png"


def sprint_and_spin(gp, method):
    gp.press_button(button=abxy_map["b"])  # Hold Sprint
    gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["up"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["right"], joystick["up"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["right"], joystick["neutral"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["right"], joystick["down"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["neutral"], joystick["down"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["left"], joystick["down"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["left"], joystick["neutral"], 0.5)
    gamepad.left_stick_and_release(gp, joystick["left"], joystick["up"], 0.5)
    gp.release_button(button=abxy_map["b"])  # Release Sprint


def usum_loop(gp, process, method, control=False, max_spins=20):
    # Similarity to control
    similarity = 1.0  # 100%

    # Move to Day Care Lady
    gamepad.left_stick_and_release(gp, joystick["right"], joystick["down"], 0.8)

    # Day Care Lady Menu
    for i in range(10):
        gamepad.press_and_release(gp, [abxy_map["a"]], 1)
        time.sleep(1)

    # Menu Escape Fallback
    for i in range(2):
        gamepad.press_and_release(gp, [abxy_map["b"]], 1)
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
    while spin_counter < max_spins and screenshot.check_for_colour(process) == False:
        # Spin twice
        for i in range(2):
            sprint_and_spin(gp)

        # Check for egg
        gamepad.press_and_release(gp, [abxy_map["a"]])

        # Increase spin counter
        spin_counter += 1

    # Egg hatched (egg menu)
    if spin_counter < max_spins:
        # Wait to reach nickname menu
        screenshot.wait_for_change(process)

        # Wait 1 second
        time.sleep(1)

        # Control not saved
        if control == False:
            # Save screenshot as 'control.png'
            screenshot.save_screenshot(process, CONTROL_SS)

            print(f"Control screenshot saved as {CONTROL_SS}.")
        else:
            # Save screenshot as 'hatched.png'
            screenshot.save_screenshot(process, HATCHED_SS)

            print(f"Encounter screenshot saved as {HATCHED_SS}.")

            print(f"Comparing {HATCHED_SS} to {CONTROL_SS} ...")
            similarity = screenshot.compare_images(HATCHED_SS, CONTROL_SS, debug=True)
            print(f"Comparison complete. Reference images saved.")
    else:
        raise Exception(f"Spin limit exceeded: {max_spins}")

    # Wait 1 second
    return similarity


def oras_loop(gp, process, method, control=False, max_loops=16):
    # Similarity to control
    similarity = 1.0  # 100%

    # Get on Mach Bike
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["y"]],  # Open Quick Menu
            [button.XUSB_GAMEPAD_DPAD_RIGHT],  # Select Mach Bike
        ],
    )

    # Move Right (Hold for 3s)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_RIGHT], 3)

    # Press 'a' button seven times
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
        ],
    )

    # Wait 4 seconds
    time.sleep(4)

    # Press 'b' button three times
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["b"]],
            [abxy_map["b"]],
            [abxy_map["b"]],
        ],
    )

    # Move Left (Hold for ~5s)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_LEFT], 5)

    # Count Loops
    loop_counter = 0

    while loop_counter < max_loops and screenshot.check_for_colour(process) == False:
        write_log(f"Starting loop '{loop_counter + 1}' ...")

        # Move Up (Hold for ~30s)
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP], 20)

        # Move Left (Hold for ~2s)
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_LEFT], 0.9)

        # Loop Up (Quick)
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP], 0.1)

        # Check for egg
        gamepad.press_and_release(gp, [abxy_map["a"]])

        # Wait 2 seconds
        time.sleep(2)

        # Increase spin counter
        loop_counter += 1

    write_log(f"Egg hatched after {loop_counter} loops.")

    # Egg hatched (egg menu)
    if loop_counter < max_loops:
        # Wait 10 seconds
        time.sleep(10)

        # Control not saved
        if control == False:
            # Save screenshot as 'control.png'
            screenshot.save_screenshot(process, CONTROL_SS)

            print(f"Control screenshot saved as {CONTROL_SS}.")
        else:
            # Save screenshot as 'hatched.png'
            screenshot.save_screenshot(process, HATCHED_SS)

            print(f"Encounter screenshot saved as {HATCHED_SS}.")

            print(f"Comparing {HATCHED_SS} to {CONTROL_SS} ...")
            similarity = screenshot.compare_images(HATCHED_SS, CONTROL_SS, debug=True)
            print(f"Comparison complete. Reference images saved.")
    else:
        raise Exception(f"Loop limit exceeded: {max_loops}")

    return similarity


def main(process, game=None, method=None, autostart=None):
    # Loops
    loops = {"usum": usum_loop, "oras": oras_loop}

    # Hatched times
    control = False
    hatched = 0

    # Similarities
    similarities = {}

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Running Egg Hatching Bot ...")

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

    # Supported game
    if game in loops:
        write_log(f"Starting for game '{game}' ...")
    else:  # Any Other Game
        raise NotImplementedError(f"Game '{game}' is unsupported!")

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

            # Load the menu for the game
            gamepad.load_game(gp, game)

            # Run the loop for the game, control var
            similarity = loops[game](gp, process, method, control)

            # Similarity as a percentage
            percentage = similarity * 100

            # Round to newest whole number
            rounded = str(round(percentage))

            write_log(f"Similarity to Control: {percentage}%, Rounded: {rounded}%")

            # Rounded not in similarity keys
            if rounded not in similarities:
                # Insert real value into array index
                similarities[rounded] = [similarity]
                input(
                    f"Unseen Rounded Similarity (Potential Shiny): Press enter to continue ..."
                )
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
                    print(
                        f"Avg. Similarity {avg_similarity}% (Potential Shiny) Found: Press enter to continue ..."
                    )
                    input("")
                else:
                    print(
                        f"New frame {avg_similarity}% similar to previous matching frames ..."
                    )

                # Insert into array index
                similarities[rounded].append(similarity)

            # Control screenshot saved
            control = True

        except Exception as e:  # Failure
            # Handle the exception depending on error
            handle_exception(e, method, autostart)

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
