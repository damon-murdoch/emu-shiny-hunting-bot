import src.gamepad as gamepad
from src.gamepad import ABXY_MAP as abxy_map
from vgamepad import XUSB_BUTTON as button

from src.log import write_log, LOG_FILE

def main(game, method):

    # Create the log file (or clear it)
    with open(LOG_FILE, "w"):
        write_log(f"Starting 'Soft Reset' Macro ...")

    # Create & configure virtual gamepad
    gp = gamepad.get_gamepad()

    # Soft reset the game (No delay)
    gamepad.soft_reset(gp, delay=0)