import constants as c
from System.form_score_calculation import calculate_form_score
import tkinter as tk

class View_Player_Details(tk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.player = player
        
        rows = [
            ("Win Percentage", self.player["win_percentage"]),
            ("Last Match Played Date", self.player["last_match_date"]),
            ("Fixtures Played This Season", self.player["fixtures_played_this_season"]),
            ("Injury Status", (self.player["injury_description"] if self.player["injury_description"] else "No Injury")),
            ("Form", round(calculate_form_score(player["user_id"]), 3))
        ]
        
        #Loop creating a "grid" of labels from rows
        for row_index, (title, value) in enumerate(rows):
            lbl_title = tk.Label(self, text=title, font=c.FONT_LABEL_BOLD, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_title.grid(row=row_index, column=0, sticky="w", padx=(10, 20), pady=6)

            lbl_value = tk.Label(self, text=value, font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, anchor="w")
            lbl_value.grid(row=row_index, column=1, sticky="w", pady=6)