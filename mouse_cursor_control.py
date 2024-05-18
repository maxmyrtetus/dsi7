import pyautogui

def move_mouse_cursor(direction):
    # Move the mouse cursor based on the detected direction
    screen_width, screen_height = pyautogui.size()
    current_x, current_y = pyautogui.position()

    # Adjust the cursor position based on the detected direction
    if direction == "up":
        new_y = max(0, current_y - 50)  # Move up by 50 pixels
        pyautogui.moveTo(current_x, new_y, duration=0.25)
    elif direction == "down":
        new_y = min(screen_height, current_y + 50)  # Move down by 50 pixels
        pyautogui.moveTo(current_x, new_y, duration=0.25)
    elif direction == "left":
        new_x = max(0, current_x - 50)  # Move left by 50 pixels
        pyautogui.moveTo(new_x, current_y, duration=0.25)
    elif direction == "right":
        new_x = min(screen_width, current_x + 50)  # Move right by 50 pixels
        pyautogui.moveTo(new_x, current_y, duration=0.25)
