import tkinter as tk
import constants as c

class Time_Entry(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bd=1, relief="solid")

        self.hours = tk.Spinbox(self, from_=0, to=23, width=2, format="%02.0f", wrap=True, bd=0, justify="center", bg=c.LIGHT_SIDEBAR, buttonbackground=c.LIGHT_SIDEBAR, highlightthickness=0)
        self.hours.pack(side="left")

        tk.Label(self, text=":", bg=c.LIGHT_SIDEBAR).pack(side="left")

        self.minutes = tk.Spinbox(self, from_=0, to=59, width=2, format="%02.0f", wrap=True, bd=0, justify="center", bg=c.LIGHT_SIDEBAR, buttonbackground=c.LIGHT_SIDEBAR, highlightthickness=0)
        self.minutes.pack(side="left")


    #Method to return the time
    def get_time(self):
        return f"{int(self.hours.get()):02d}:{int(self.minutes.get()):02d}"


    #Method to set the time
    def set_time(self, time):
        hours, minutes = time.split(":")

        self.hours.delete(0, tk.END)
        self.hours.insert(0, hours)

        self.minutes.delete(0, tk.END)
        self.minutes.insert(0, minutes)
        
        