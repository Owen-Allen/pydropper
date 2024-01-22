#!/usr/local/bin/python3.10
import pyautogui
import tkinter as tk
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

# https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
def convert_rgb_to_names(rgb_tuple):
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def rgb_to_hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def get_rgb_at_mouse():
    x, y = pyautogui.position()
    r, g, b = pyautogui.pixel(x * 2, y * 2) # for some reason on mac, x and y need to be doubled https://stackoverflow.com/questions/72157805/pyautogui-not-showing-correct-pixel-color-on-mac/77020255#77020255
    return r, g, b

def update_labels():
    r, g, b = get_rgb_at_mouse()
    color_name = convert_rgb_to_names((r,g,b))
    hex = rgb_to_hex(r,g,b)
    name_label.config(text=color_name)
    hex_label.config(text=hex)
    window.after(100, update_labels)

def main():
    global window, name_label, hex_label
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

    window.mainloop()

if __name__ == "__main__":
    main()
