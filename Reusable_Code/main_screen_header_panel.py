import tkinter as tk
import constants as c

#Class that can be imported in the main screen files which create the header bar
class Header_Panel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=c.LIGHT_PRIMARY_ACCENT, height=80)
        self.pack_propagate(False)

        #Create the title and puts it on the left
        self.lbl_title = tk.Label(self, text="Sport's Team Management", font=c.FONT_HEADING, bg=c.LIGHT_PRIMARY_ACCENT, fg="white")
        self.lbl_title.pack(side="left", padx=20)