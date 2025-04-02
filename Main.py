from tkinter import *
from PIL import Image, ImageTk
import time
import psutil
import win32api
import win32con
import pywintypes
import threading  # Import threading module
import screen_brightness_control as sbc
import subprocess

root = Tk()
root.title("Refresh Rate Controller")
root.geometry("300x270+1300+150")
root.resizable(False, False)
root.configure(bg="black")

def change_refresh_rate(refresh_rate):
    try:
        devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        devmode.DisplayFrequency = refresh_rate
        result = win32api.ChangeDisplaySettings(devmode, win32con.CDS_UPDATEREGISTRY)

        if result == win32con.DISP_CHANGE_SUCCESSFUL:
            l3.config(text=f"Refresh rate changed to {refresh_rate}Hz successfully!")
        elif result == win32con.DISP_CHANGE_RESTART:
            l3.config(text="System needs a restart to apply changes.") 
        else:
            l3.config(text="Failed to change refresh rate.") 
    except pywintypes.error as e:
        print(f"Error: {e}")

def check_battery_status():
    battery = psutil.sensors_battery()
    if battery is not None:
        return battery.power_plugged  # True if plugged in, False if on battery
    return None  # Battery info not available
def close_app():
    root.destroy()
def run():
    Btn_run.config(text="Running")
    Btn_run.config(command="")
    Btn_exit = Button(root, text="Exit", font=("bold", 14, "bold"), bd=0, fg="black", command=close_app)
    Btn_exit.pack(pady=20)
    current_brightness = sbc.get_brightness()
    def loop_function():
        while True:
            if check_battery_status() is False:
                l2.config(text="Laptop is running on battery")
                new_brightness = max(10, current_brightness[0] - 80) 
                sbc.set_brightness(new_brightness)
                l4.config(text=f"Brightness set to {new_brightness}%")
                change_refresh_rate(60) 
                subprocess.run(["DisplaySwitch.exe", "/internal"])
                l5.config(text="Display mode set to 'PC Screen Only'")
            elif check_battery_status() is True:
                l2.config(text="Laptop is plugged in")
                new_brightness = max(80, current_brightness[0] - 20)
                l4.config(text=f"Brightness set to {new_brightness}%") 
                sbc.set_brightness(new_brightness)
                change_refresh_rate(165)
                subprocess.run(["DisplaySwitch.exe", "/extend"])
                l5.config(text="Display mode set to 'Extend'")
            time.sleep(10)  # Change to 10 seconds instead of 1000 to make it work properly

    # Run the loop in a separate thread
    threading.Thread(target=loop_function, daemon=True).start()

Icon = Image.open("rate2.jpg")
icon = ImageTk.PhotoImage(Icon)
root.iconphoto(False, icon)

Label(root, text="Refresh Rate Regulator", font=("arial", 13, "bold"), bg="black", fg="white").pack()
Btn_run = Button(root, text="Run", font=("bold", 14, "bold"), bd=0, fg="black", command=run)
Btn_run.pack(pady=20)
l2 = Label(root, text="Waiting for status...", font=("arial", 10, "bold"), bg="black", fg="white")
l2.pack()
l3 = Label(root, text="", font=("arial", 10, "bold"), bg="black", fg="white")
l3.pack()
l4 = Label(root, text="", font=("arial", 10, "bold"), bg="black", fg="white")
l4.pack()
l5 = Label(root, text="", font=("arial", 10, "bold"), bg="black", fg="white")
l5.pack()

root.mainloop()
