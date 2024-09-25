import argparse

import src.screenshot as screenshot
import src.gamepad as gamepad
import src.window as window
import src.macro as macro
import src.bot as bot

TITLE = "3DS Emulator Shiny Hunting Bot"

GAMES = [
    "usum",
    "oras",
    "xy",
]

OPTIONS = {
    # Setup
    "setup": gamepad.configure_citra,
    # Macros
    "premier-ball": macro.premier_ball,
    "quick-release": macro.quick_release,
    # Bots
    "soft-reset-bot": bot.soft_reset_bot,
    "egg-hatching-bot": bot.egg_hatching_bot,
}

parser = argparse.ArgumentParser("n3ds.py", description=TITLE)
parser.add_argument("action", choices=list(OPTIONS.keys()))
parser.add_argument("-g", "--game", choices=GAMES, default=GAMES[0])
parser.add_argument("-a", "--autostart", default=None)

if __name__ == "__main__":

    try:
        # Citra window
        citra = None

        # Parse the command-line args
        arguments = parser.parse_args()

        print(f"Starting {TITLE} ...")

        # Find the citra window
        citra = window.find_window()

        # No window found, and autostart is setup
        if citra == None and arguments.autostart:
            # Start the process using the autostart script
            citra = window.start_window(arguments.autostart)

        # Citra window found
        if citra:
            # Take a screenshot of the citra window
            filename = screenshot.save_screenshot(citra, "test.png")

            print("Screenshot has been saved as 'test.png'.")
            print("Please confirm the screenshot dimensions are accurate.")

            # Run the function for the selected option
            option_script = OPTIONS[arguments.action](
                # Include auto-start script (Not available for all macros)
                citra,
                game=arguments.game,
                autostart=arguments.autostart,
            )

        else:  # No window
            raise Exception("Window not found!")

    except Exception as e:
        print(f"Failed to start {TITLE}! {e}")
