import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button

#Class that can be imported to add a sidebar to the screen
class main_screen_sidebar(tk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent, bg=c.LIGHT_SIDEBAR, width=200)
        self.pack_propagate(False)
        self.pack(side="left", fill="y")
        
        self.btn_frame = tk.Frame(self, bg=c.LIGHT_SIDEBAR)
        self.btn_frame.pack(expand=False)
        
        #Create buttons for all items inside the buttons tuple
        for text, command in buttons:
            btn = Rounded_Button(self.btn_frame, text=text, command=command, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_SIDEBAR)
            btn.pack(pady=15)