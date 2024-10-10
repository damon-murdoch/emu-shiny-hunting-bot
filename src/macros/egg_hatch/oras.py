import math
import time
import src.gamepad as gamepad
from vgamepad import XUSB_BUTTON as button
from src.gamepad import ABXY_MAP as abxy_map

from src.common import get_execution_time

# Flame Body Multiplier
FLAME_BODY_MULTIPLIER = 2

# Seconds to hold 'up' per loop
SECONDS_PER_LOOP = 40

# Default Step Counter
DEFAULT_STEPS = 10280

# Steps Per Resort Lap
RESORT_STEPS = 256

# Min. Loops Per Egg
MIN_LOOPS = 3


def get_loop_count(steps=DEFAULT_STEPS):
    return math.ceil(steps / (RESORT_STEPS * FLAME_BODY_MULTIPLIER))


def deposit_mon(gp, delay=4, menu_delay=2, change_box=False):

    # Refresh the location
    refresh_location(gp)

    # Enter Pokemon Centre
    gamepad.press_and_release_sequence(
        gp,
        [
            [button.XUSB_GAMEPAD_DPAD_UP],  # Face Pokemon Center
            [button.XUSB_GAMEPAD_DPAD_UP],  # Enter Pokemon Center
        ],
    )

    # Wait for load
    time.sleep(delay)

    # Hold up on the d-pad for 3 seconds (to reach the counter)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP], 2.4)

    # Hold left on the d-pad for 1 second (to reach the pc)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_RIGHT], 0.4)

    # Wait 1 second
    time.sleep(1)

    # Face the computer and start the PC
    gamepad.press_and_release_sequence(
        gp,
        [
            [button.XUSB_GAMEPAD_DPAD_UP],  # Face computer
            [abxy_map["a"]],  # Start PC
        ],
    )

    # Wait for load
    time.sleep(delay)

    # Interact with PC
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["a"]],  # Boot Screen
            [abxy_map["a"]],  # Lanette's PC
            [button.XUSB_GAMEPAD_DPAD_DOWN],
            [abxy_map["a"]],  # Deposit Menu
            [button.XUSB_GAMEPAD_DPAD_RIGHT],
            [abxy_map["a"]],  # Select Pokemon
            [abxy_map["a"]],  # Select Deposit
        ],
        delay_sequence=menu_delay
    )

    # Change Box
    if change_box:
        # Switch to the next (right) box
        gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_RIGHT_SHOULDER])
        time.sleep(menu_delay)

    # Exit Menu
    gamepad.press_and_release_sequence(
        gp,
        [
            # Confirm Box
            [abxy_map["a"]], 
            # Exit Menu
            [abxy_map["b"]],
            [abxy_map["b"]],
            [abxy_map["b"]],
            [abxy_map["b"]],
        ],
        delay_sequence=menu_delay
    )

    # Wait for load
    time.sleep(delay)

    # Hold right on the d-pad for 1 second (to reach the counter)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_LEFT], 0.4)

    # Hold down on the d-pad for 3 seconds (to reach the exit)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_DOWN], 2.4)

    # Wait for load
    time.sleep(delay)


def hatch_egg(gp, delay=24, end_delay=6):

    # Start egg hatching screen

    # Hatch the egg
    gamepad.press_and_release(gp, [abxy_map["a"]])

    # Wait for animation
    time.sleep(delay)

    # Do not nickname the Pokemon
    gamepad.press_and_release(gp, [abxy_map["b"]])

    # Wait for close
    time.sleep(end_delay)


def receive_egg(gp):

    # Refresh the location
    refresh_location(gp)

    # Equip the mach bike
    equip_mach_bike(gp)

    # Move Right (Hold for 3s)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_RIGHT], 3)

    # Collect the egg from the day-care man
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

    # Exit the egg collection menu
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["b"]],
            [abxy_map["b"]],
        ],
    )


def equip_mach_bike(gp):

    # Get on Mach Bike
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["y"]],  # Open Quick Menu
            [button.XUSB_GAMEPAD_DPAD_RIGHT],  # Select Mach Bike
        ],
    )


def refresh_location(gp, delay=14):

    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["y"]],  # Quick Menu
            [button.XUSB_GAMEPAD_DPAD_UP],  # Eon Flute
            [abxy_map["a"]],  # Eon Flute
        ],
    )

    # Wait for animation
    time.sleep(delay)

    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["a"]],  # Land at location
            [abxy_map["a"]],  # Confirm
        ],
    )

    # Wait for animation
    time.sleep(delay)


def resort_loop(gp, loops=16):

    # Move back to Pokemon Center
    refresh_location(gp)

    # Get on mach bike
    equip_mach_bike(gp)

    # Move Left (Hold for ~2s)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_LEFT], 2)

    # Loops * avg. time per loop (~30s+)
    duration = loops * SECONDS_PER_LOOP

    # Move Up (Hold for 'duration' seconds)
    gamepad.press_and_release(gp, [button.XUSB_GAMEPAD_DPAD_UP], duration)


@get_execution_time
def egg_hatch_loop(gp, loops, hatched):

    # Check for egg
    receive_egg(gp)

    # Loop resort (hatch egg)
    resort_loop(gp, loops)

    # Egg hatching sequence
    hatch_egg(gp)

    # Check if the box capacity has been reached
    change_box = hatched > 0 and hatched % 30 == 0

    # Deposit Egg (Switching box if necessary)
    deposit_mon(gp, change_box=change_box)


def main(gp):

    print(
        f"Enter the number of steps required to hatch your Pokemon (Default: {DEFAULT_STEPS})"
    )
    print("This will determine the number of resort loops required per egg.")

    # Default Steps
    steps = DEFAULT_STEPS

    try:
        steps = int(input("Required Steps: "))
    except:  # Invalid Input
        pass

    # Get the loops for the step count (or min. loops)
    loops = max(get_loop_count(steps), MIN_LOOPS)

    print(f"{steps} steps -> {loops} loops ...")

    # Eggs Hatched
    hatched = 0

    # Loop resort (wait for egg)
    resort_loop(gp, loops=MIN_LOOPS)

    try:

        # Infinte
        while True:
            # Perform main loop
            egg_hatch_loop(gp, loops, hatched)

            # Increment counter
            hatched += 1
    except Exception as e:
        print(f"Egg hatching bot failed! {str(e)}")
