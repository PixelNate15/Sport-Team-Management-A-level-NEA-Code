import constants as c
import tkinter as tk

class Main_Screen_Captain(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id

        
        self.lbl_main_title = tk.Label(self, text="Sport's Team Management Captain", font=c.FONT_TITLE, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_main_title.pack(pady=(0,25))