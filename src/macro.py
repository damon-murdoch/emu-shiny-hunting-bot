import os, time, random
from datetime import datetime

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.window as window

from vgamepad import XUSB_BUTTON as button

from src.gamepad import JOYSTICK_COORDINATES as joystick
from src.log import write_log, LOG_FILE

def premier_ball(window, game=None, autostart=None):

    def buy_premier_ball(gp):
        gamepad.press_and_release_sequence(gp, [
            [button.XUSB_GAMEPAD_B], # Select PokeBall
            [button.XUSB_GAMEPAD_DPAD_RIGHT], # Increase count by 10
            [button.XUSB_GAMEPAD_DPAD_DOWN], # Decrease count by 1
            [button.XUSB_GAMEPAD_B], # Select ball count
            [button.XUSB_GAMEPAD_B], # Confirm ball count
            # Dialog Boxes
            [button.XUSB_GAMEPAD_B],
            [button.XUSB_GAMEPAD_B],
            [button.XUSB_GAMEPAD_B],
        ], 1)

    # Bot Version
    version = "1.0.0"

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting Premier Ball Macro v{version} ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    print("Please start this script from the 'buy' menu at any Pokemon Center.")

    count = 1
    try:
        count = int(input("Enter the number of Premier Balls to purchase: "))
        print(f"{count} Premier Balls will be purchased.")
    except Exception as e:
        print(f"One Premier Ball will be purchased.")

    # Release 'count' pokemon:
    for index in range(count):
        buy_premier_ball(gp)

def quick_release(window, game=None, autostart=None):

    def release_mon(gp):
        # Open menu, release pokemon, close menu
        gamepad.press_and_release_sequence(
            gp,
            [
                [button.XUSB_GAMEPAD_B],
                [button.XUSB_GAMEPAD_DPAD_UP],
                [button.XUSB_GAMEPAD_DPAD_UP],
                [button.XUSB_GAMEPAD_B],
                [button.XUSB_GAMEPAD_DPAD_UP],
                [button.XUSB_GAMEPAD_B],
                [button.XUSB_GAMEPAD_B],
                [button.XUSB_GAMEPAD_B],
            ],
            1,
        )

    # Bot Version
    version = "1.0.0"

    # Create the log file (or clear it)
    with open(LOG_FILE, "w") as file:
        write_log(f"Starting Quick Release Bot v{version} ...")

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
        release_mon(gp)

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

