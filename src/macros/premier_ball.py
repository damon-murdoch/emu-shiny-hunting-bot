import src.gamepad as gamepad
from src.gamepad import ABXY_MAP as abxy_map
from vgamepad import XUSB_BUTTON as button

from src.log import write_log, LOG_FILE


def buy_premier_ball(gp, method):
    gamepad.press_and_release_sequence(
        gp,
        [
            [abxy_map["a"]],  # Select PokeBall
            [button.XUSB_GAMEPAD_DPAD_RIGHT],  # Increase count by 10
            [button.XUSB_GAMEPAD_DPAD_DOWN],  # Decrease count by 1
            [abxy_map["a"]],  # Select ball count
            [abxy_map["a"]],  # Confirm ball count
            # Dialog Boxes
            [abxy_map["a"]],
            [abxy_map["a"]],
            [abxy_map["a"]],
        ]
    )


def main(game, method):
    # Create the log file (or clear it)
    with open(LOG_FILE, "w"):
        write_log(f"Starting Premier Ball Macro ...")

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
    for _ in range(count):
        buy_premier_ball(gp, method)
