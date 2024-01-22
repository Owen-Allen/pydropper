import pyautogui
import tkinter as tk
import threading
import time
import pyperclip
from pynput import keyboard
from color_utils import ColorConverter  # A separate module for color conversion logic

class ColorPickerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.setup_window()
        self.setup_labels()
        self.converter = ColorConverter()
        self.update_labels()
        self.start_keyboard_listener()

    def setup_window(self):
        self.window.title('')
        self.window.geometry("200x60")
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.8)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_labels(self):
        self.name_label = tk.Label(self.window, font=("Futura", "16", ""))
        self.name_label.pack(expand=True, fill='both', anchor='w')
        self.hex_label = tk.Label(self.window, font=("Futura", "16", ""))
        self.hex_label.pack(expand=True, fill='both', anchor='w')

    def update_labels(self):
        r, g, b = self.get_rgb_at_mouse()
        color_name = self.converter.convert_rgb_to_names((r, g, b))
        hex_color = self.converter.rgb_to_hex(r, g, b)
        self.name_label.config(text=color_name)
        self.hex_label.config(text=hex_color)
        self.window.after(10, self.update_labels)

    def get_rgb_at_mouse(self):
        x, y = pyautogui.position()
        return pyautogui.pixel(x * 2, y * 2)

    def start_keyboard_listener(self):
        self.stop_event = threading.Event()
        self.listener_thread = threading.Thread(target=self.keyboard_event_listener)
        self.listener_thread.start()

    def keyboard_event_listener(self):
        def on_press(key):
            try:
                if key.char == 'ç':
                    pyperclip.copy(self.hex_color)
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while not self.stop_event.is_set():
            time.sleep(0.1)  # Short delay to reduce CPU usage

        listener.stop()


    def on_closing(self):
        self.stop_event.set()
        self.listener_thread.join()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ColorPickerApp()
    app.run()
