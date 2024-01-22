import pyautogui
import tkinter as tk
from scipy.spatial import KDTree
from webcolors import (CSS3_HEX_TO_NAMES, hex_to_rgb)
import pyperclip
from pynput import keyboard
import threading

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

def on_press(key):
    global hex_color
    if key == keyboard.KeyCode.from_char('ç'):
        pyperclip.copy(hex_color)

def start_listener(stop_event):
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

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
    update_labels()  # Start updating the label

    # Threading for user input
    stop_event = threading.Event()
    listener_thread = threading.Thread(target=start_listener, args=(stop_event,))
    listener_thread.start()

    def on_closing():
        stop_event.set()  # close the listener_thread when the tkinter window is closed
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

if __name__ == "__main__":
    main()
