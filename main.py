import pygetwindow as pgw

import src.screenshot as screenshot

# Bots
import src.bot as bot

options = [
    "Static Encounter Bot",
    "Egg Hatcher (XY)",
    "Egg Hatcher (ORAS)",
    "Egg Hatcher (SM/USUM)",
]

if __name__ == "__main__":

    try:
        print("Starting shiny hunting bot ...")

        # Citra window
        citra = None

        windows = pgw.getAllWindows()
        for window in windows:
            title = window.title
            if title.startswith("Citra"):
                citra = window

        # Citra window found
        if citra:
            # Take a screenshot of the citra window
            filename = screenshot.save_screenshot(citra, "test.png")

            print("Please confirm the screenshot dimensions are accurate.")

            print("Available Modes:")
            for i in range(len(options)):
                text = options[i]
                print(f"{i + 1}: {text}")
            print(f"{i + 2}: Exit")

            # Selected Option
            option = 0

            try:
                option = int(input("Please select an option: ")) - 1
            except Exception as e:
                option = -1  # Bad input

            # Within the range of options
            if option >= 0 and option < len(options):
                if option == 0:  # Configure Gamepad (Citra)
                    bot.static_encounter_bot(citra)
                else:  # Not Implemented
                    print("TODO: Implement this")
            else:  # Outside of the range
                print("Goodbye!")

        else:  # No citra window
            raise Exception("Citra window not found!")

    except Exception as e:
        print(f"Failed to start citra shiny hunting bot! {e}")
