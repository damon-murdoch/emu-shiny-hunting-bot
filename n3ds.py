import argparse

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.window as window

# Macros
from src.macros.soft_reset import main as srm
from src.macros.premier_ball import main as pbm
from src.macros.egg_hatching import main as ehm
from src.macros.quick_release import main as qrm

# Bots
from src.bots.egg_hatching import main as ehb
from src.bots.static_encounter import main as seb

from src.classes import Macro, Bot

TITLE = "3DS Controller Input Bot"

VERSION = "1.0.0"

GAMES = [
    "usum",
    "oras",
]

METHODS = ["emulator", "remote"]

ACTIONS = {
    # Setup
    "setup": Macro(gamepad.configure_citra),
    # Macros
    "soft-reset": Macro(srm),
    "egg-hatching": Macro(ehm),
    "premier-ball": Macro(pbm),
    "quick-release": Macro(qrm),
    # Bots
    "egg-hatching-bot": Bot(ehb),
    "static-encounter-bot": Bot(seb),
}

parser = argparse.ArgumentParser("n3ds.py", description=TITLE)
parser.add_argument(
    "action", choices=list(ACTIONS.keys()), help="The macro or bot which should be run"
)
parser.add_argument(
    "-m",
    "--method",
    choices=METHODS,
    help="Method for which the script should run (i.e. emulator, remote-play, etc)",
    required=True,
)
parser.add_argument(
    "-g",
    "--game",
    choices=GAMES,
    help="Game for which the selected script should run",
    required=True,
)
parser.add_argument(
    "-a",
    "--autostart",
    default=None,
    help="Auto-Start Script for starting / restarting the game window on startup or after a crash",
)
parser.add_argument(
    "-w",
    "--window",
    default=None,
    help="Custom window title for the emulator / capture window, e.g. 'Citra' -> 'Citra 5115f64 | ...'",
)

if __name__ == "__main__":
    try:
        print(f"Starting {TITLE} v{VERSION} ...")

        # Parse command-line arguments
        arguments = parser.parse_args()

        # Get the action selected
        action = ACTIONS[arguments.action]

        # Is Macro (Headless)
        if action.is_macro():
            # Run the script for the action
            result = action.run(arguments.game, arguments.method)

        else:  # Window required
            # Custom window provided
            if arguments.window:
                print(f"Custom window filter provided: {arguments.window} ...")

                # Set the custom window title
                window.set_window_title(arguments.method, arguments.window)

            print(
                f"Searching for window title starting with '{window.get_window_title(arguments.method)}' ..."
            )

            # Find the game window
            process = window.find_window(arguments.method)

            # No window found, and autostart is setup
            if process == None and arguments.autostart:
                # Start the process using the autostart script
                process = window.start_window(arguments.autostart, arguments.method)

            # game window found
            if process:
                # Take a screenshot of the game window
                filename = screenshot.save_screenshot(process, "test.png")

                print("Screenshot has been saved as 'test.png'.")
                print("Please confirm the screenshot dimensions are accurate.")

                # Run the script for the action
                result = action.run(
                    arguments.game, arguments.method, process, arguments.autostart
                )

            else:  # No window
                raise Exception("Window not found!")

    except Exception as e:
        print(f"Failed to start {TITLE}! {e}")
