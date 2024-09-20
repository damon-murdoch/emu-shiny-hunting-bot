import pygetwindow as pgw
import argparse

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.bot as bot

TITLE="3DS Emulator Shiny Hunting Bot"

GAMES = [
    "usum",
    "oras",
    "xy",
]

OPTIONS = {
    "setup": gamepad.configure_citra,
    "static": bot.static_encounter_bot,
}

parser = argparse.ArgumentParser(
    "n3ds.py", description=TITLE
)
parser.add_argument("-g", "--game", choices=GAMES, default=GAMES[0])
parser.add_argument("action", choices=list(OPTIONS.keys()))
parser.add_argument("-w", "--window", default="Citra")

if __name__ == "__main__":

    try:
        # Citra window
        citra = None

        # Parse the command-line args
        arguments = parser.parse_args()

        print(f"Starting {TITLE} ...")

        windows = pgw.getAllWindows()
        for window in windows:
            title = window.title
            if title.startswith(arguments.window):
                citra = window

        # Citra window found
        if citra:
            # Take a screenshot of the citra window
            filename = screenshot.save_screenshot(citra, "test.png")

            print("Screenshot has been saved as 'test.png'.")
            print("Please confirm the screenshot dimensions are accurate.")

            # Run the function for the selected option
            option_script = OPTIONS[arguments.action](citra, game=arguments.game)

        else:  # No window
            raise Exception("Window not found!")

    except Exception as e:
        print(f"Failed to start {TITLE}! {e}")
