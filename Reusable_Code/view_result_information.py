import constants as c
import tkinter as tk

class View_Result_Details(tk.Frame):
    def __init__(self, parent, result):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.result = result
    
        
        rows = [
            ("Result", (f"{self.result["sets_won"]} - {self.result["sets_lost"]} ")),
            ("Opposition", self.result["opposition"]),
            ("Date", self.result["date"]),
            ("Home/Away", self.result["home_away"]),
            ("Division", self.result["division"]),
            ("Notes", self.result["notes"]),
        ]
        
        #Loop creating a "grid" of labels from rows
        for row_index, (title, value) in enumerate(rows):
            lbl_title = tk.Label(self, text=title, font=c.FONT_LABEL_BOLD, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_title.grid(row=row_index, column=0, sticky="w", padx=(10, 20), pady=6)

            lbl_value = tk.Label(self, text=value, font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_value.grid(row=row_index, column=1, sticky="w", pady=6)