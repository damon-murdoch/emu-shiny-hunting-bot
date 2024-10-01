import pygetwindow as pgw
import time

from subprocess import Popen as subprocess

# Window Title
WINDOW_TITLE = {"emulator": "Citra", "remote": "Snickerstream - "}

# Startup Wait Time
STARTUP_DELAY = 5


def find_window(method):
    windows = pgw.getAllWindows()
    for window in windows:
        title = window.title
        if title.startswith(WINDOW_TITLE[method]):
            return window
    return None


def start_window(script, method, delay=STARTUP_DELAY):

    # Run the autostart script
    subprocess(script, shell=True)

    # Wait 5 seconds
    time.sleep(delay)

    # Find the citra window
    return find_window(method)
