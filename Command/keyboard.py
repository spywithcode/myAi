from pynput.keyboard import Key, Controller
from time import sleep
from voice_commands import speak, query

# Initialize the keyboard controller
keyboard = Controller()

def volume_up(steps: int = 10, delay: float = 0.1):
    """
    Increase the system volume.

    Args:
        steps (int): Number of volume up presses.
        delay (float): Delay between each press in seconds.
    """
    for _ in range(steps):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(delay)

def volume_down(steps: int = 10, delay: float = 0.1):
    """
    Decrease the system volume.

    Args:
        steps (int): Number of volume down presses.
        delay (float): Delay between each press in seconds.
    """
    for _ in range(steps):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(delay)
