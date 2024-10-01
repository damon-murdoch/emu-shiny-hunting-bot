import time
import src.gamepad as gamepad

from src.gamepad import ABXY_MAP as abxy
from vgamepad import XUSB_BUTTON as button
from src.log import write_log, LOG_FILE


def release_mon(gp, method):
    # Open menu, release pokemon, close menu
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy[method]["a"]],
            [button.XUSB_GAMEPAD_DPAD_UP],
            [button.XUSB_GAMEPAD_DPAD_UP],
            [abxy[method]["a"]],
            [button.XUSB_GAMEPAD_DPAD_UP],
            [abxy[method]["a"]],
            [abxy[method]["a"]],
            [abxy[method]["a"]],
        ],
        1,
    )


def main(game, method):
    # Create the log file (or clear it)
    with open(LOG_FILE, "w"):
        write_log(f"Starting Quick Release Bot ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    print("Start this script from the top-left most position in the leftmost box.")
    print("Please ensure boxes are full from the top-left to top-right first.")

    count = 1
    try:
        count = int(input("Enter the number of Pokemon to release: "))
        print(f"{count} pokemon will be released.")
    except Exception as e:
        print(f"Releasing selected Pokemon only.")

    # Move controller right
    move_right = True

    # Release 'count' pokemon:
    for index in range(count):
        # Box slot number
        slot = index + 1

        print(f"Releasing pokemon {index + 1} ...")

        # Release Pokemon
        release_mon(gp, method)

        # Moving to new box
        if slot % 30 == 0:
            gamepad.press_and_release_sequence(
                gp,
                [
                    # Switch page
                    [button.XUSB_GAMEPAD_RIGHT_SHOULDER],
                    # Reset to left
                    [button.XUSB_GAMEPAD_DPAD_RIGHT],
                    [button.XUSB_GAMEPAD_DPAD_RIGHT],
                    [button.XUSB_GAMEPAD_DPAD_RIGHT],
                    # Reset to top
                    [button.XUSB_GAMEPAD_DPAD_DOWN],
                    [button.XUSB_GAMEPAD_DPAD_DOWN],
                    [button.XUSB_GAMEPAD_DPAD_DOWN],
                ],
            )

        # Moving to new row
        elif slot % 6 == 0:
            gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_DOWN])
            # Toggle move left/right
            move_right = not move_right
            # Wait 1 second
            time.sleep(1)

        # Not last release
        elif slot != count:
            if move_right:
                gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_RIGHT])
            else:
                gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_LEFT])

    time.sleep(1)
