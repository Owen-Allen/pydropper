import pyautogui
import tkinter as tk
from scipy.spatial import KDTree
from webcolors import (CSS3_HEX_TO_NAMES, hex_to_rgb)
import pyperclip
from pynput import keyboard
import threading
import time

# initialize color data for convert_rgb_to_names
names = []
rgb_values = []
for color_hex, color_name in CSS3_HEX_TO_NAMES.items():
    names.append(color_name)
    rgb_values.append(hex_to_rgb(color_hex))
kdt_db = KDTree(rgb_values)

def convert_rgb_to_names(rgb_tuple):
    # https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def rgb_to_hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def get_rgb_at_mouse():
    x, y = pyautogui.position()
    r, g, b = pyautogui.pixel(x * 2, y * 2) # for some reason on mac, x and y need to be doubled https://stackoverflow.com/questions/72157805/pyautogui-not-showing-correct-pixel-color-on-mac/77020255#77020255
    return r, g, b

def update_labels():
    global hex_color
    r, g, b = get_rgb_at_mouse()
    color_name = convert_rgb_to_names((r,g,b))
    hex_color = rgb_to_hex(r,g,b)
    name_label.config(text=color_name)
    hex_label.config(text=hex_color)
    window.after(10, update_labels)

def keyboard_event_listener(stop_event):
    def on_press(key):
        if key == keyboard.KeyCode.from_char('ç'):
            pyperclip.copy(hex_color)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while not stop_event.is_set():
        time.sleep(0.1)  # Check for the stop_event every 0.1 seconds

    listener.stop()

def main():
    global window, name_label, hex_label, hex_color
    window = tk.Tk()
    window.title('')
    window.geometry("200x60")
    window.attributes("-topmost", True)
    window.attributes("-alpha", 0.8)

    name_label = tk.Label(window, font=("Futura", "16", ""))
    name_label.pack(expand=True, fill='both', anchor='w')
    hex_label = tk.Label(window, font=("Futura", "16", ""))
    hex_label.pack(expand=True, fill='both', anchor='w')

    # start window event loop
    update_labels()

    # start threading for user input
    stop_event = threading.Event()
    listener_thread = threading.Thread(target=keyboard_event_listener, args=(stop_event,))
    listener_thread.start()

    def on_closing():
        # cleanup keyboard listener before closing window
        stop_event.set()
        listener_thread.join()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

if __name__ == "__main__":
    main()
