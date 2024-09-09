import time
import vgamepad as vg
from vgamepad import XUSB_BUTTON as button

# Joystick Coordinates
JOYSTICK_COORDINATES = {
    "up": 1.0,
    "down": -1.0, 
    "left": -1.0, 
    "right": 1.0,
    "neutral": 10
}

def left_stick_and_release(gp, x, y, delay: int = 0.01):
    
    # Input the left joystick
    gp.left_joystick_float(x_value_float=x, y_value_float=y)
    gp.update()

    # Wait for delay (if set)
    if delay: 
        time.sleep(delay)

    # Reset the left joystick
    gp.left_joystick_float(x_value_float=0, y_value_float=0)
    gp.update()


def press_and_release(gp, buttons, delay: int = 0.01):

    # Press button and update
    for button in buttons:
        gp.press_button(button=button)
    gp.update()

    # Wait for delay (if set)
    if delay:
        time.sleep(delay)

    # Release button and update
    for button in buttons:
        gp.release_button(button=button)
    gp.update()


def press_and_release_sequence(
    gp, sequence, delay_sequence: int = 0.05, delay_buttons: int = 0.01
):

    # Loop over the sequence elements
    for buttons in sequence:
        # Press and release the buttons, wait for delay
        press_and_release(gp, buttons, delay_buttons)
        if delay_sequence:
            time.sleep(delay_sequence)


def get_gamepad():

    # Create virtual gamepad
    gp = vg.VX360Gamepad()

    return gp


def configure_citra(gp=None):

    # Create new gamepad, if not provided
    if gp == None:
        gp = get_gamepad()

    print("Go to Emulation -> Configure -> Controls and click 'Auto Map' ...")
    print(
        "Warning: This will overwrite your config! If you would like to create a new Citra profile, please do this now."
    )

    input("After clicking 'OK', press enter:")
    press_and_release(gp, button.XUSB_GAMEPAD_A)
