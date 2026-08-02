import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
import tkinter as tk

class View_Fixture_Details(tk.Frame):
    def __init__(self, parent, fixture):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.fixture = fixture
    
        
        rows = [
            ("Opposition", self.fixture["opposition"]),
            ("Date", self.fixture["date"]),
            ("Start Time", self.fixture["start_time"]),
            ("Location", self.fixture["location"]),
            ("Home/Away", self.fixture["home_away"]),
            ("Division", self.fixture["division"]),
            ("Notes", self.fixture["notes"])
        ]
        
        #Loop creating a "grid" of labels from rows
        for row_index, (title, value) in enumerate(rows):
            lbl_title = tk.Label(self, text=title, font=c.FONT_LABEL_BOLD, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_title.grid(row=row_index, column=0, sticky="w", padx=(10, 20), pady=6)

            lbl_value = tk.Label(self, text=value, font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_value.grid(row=row_index, column=1, sticky="w", pady=6)