import constants as c
import tkinter as tk

class View_Injury_Details(tk.Frame):
    def __init__(self, parent, injury = None):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.injury = injury
    
        if self.injury:
            self.can_you_play_text = ("Yes" if self.injury["can_play"] == 1 else "No")
            rows = [
                ("Injury", self.injury["description"]),
                ("Return Date", self.injury["expected_end_date"]),
                ("Can you play", self.can_you_play_text),
                ("Notes", self.injury["notes"]),

            ]
        else:
            rows = [
                ("Injury", "None"),
                ("Return Date", "None"),
                ("Can you play", "Yes"),
                ("Notes", "None"),

            ]
        
        #Loop creating a "grid" of labels from rows
        for row_index, (title, value) in enumerate(rows):
            lbl_title = tk.Label(self, text=title, font=c.FONT_LABEL_BOLD, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_title.grid(row=row_index, column=0, sticky="w", padx=(10, 20), pady=6)

            lbl_value = tk.Label(self, text=value, font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_value.grid(row=row_index, column=1, sticky="w", pady=6)