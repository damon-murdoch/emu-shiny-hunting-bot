import src.window as window

from src.log import write_log


def handle_exception(e, method, autostart=None):
    # Error msg string
    errmsg = str(e)

    # Full error string
    message = f"Exception: {e}"

    # Window has crashed
    if errmsg.startswith("Error code from Windows: 1400 - Invalid window handle."):

        # No window
        process = None

        # Autostart Enabled
        if autostart:
            write_log(f"{message} Restarting ...")

            # Return new window
            process = window.start_window(autostart, method)
        # Remotely connected to console
        elif method == "remote":
            write_log(f"Remote capture disconnected.")
            input("Please reconnect and press enter:")

            # Attempt to find the new window
            process = window.find_window(method)

        # Window found
        if process:
            # Return new window
            return process
        else:
            # Failed to create window
            raise Exception(message)

    else:  # Generic error
        write_log(f"{message}, Resetting ...")
