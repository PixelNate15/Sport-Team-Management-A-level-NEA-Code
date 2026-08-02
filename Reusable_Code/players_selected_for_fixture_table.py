import constants as c
from Reusable_Code.Rounded_Items.rounded_shapes import draw_rounded_rect
from SQL import get_players_for_fixture
import tkinter as tk


#Class that draws a single rounded table showing both pairs selected for a fixture
class Team_Selection_Table(tk.Canvas):
    def __init__(self, parent, fixture_id, width=500, height=160, radius=16, bg_colour=c.LIGHT_SIDEBAR, parent_bg_colour=c.LIGHT_BACKGROUND):
        super().__init__(parent, width=width, height=height, bg=parent_bg_colour, highlightthickness=0)
        
        self.width = width
        self.height = height
        
        draw_rounded_rect(self, 0, 0, width, height, radius, bg_colour)
        
        #Draw internal divider lines on top
        self.create_line(width / 2, radius, width / 2, height - radius, fill=c.LIGHT_BORDER, width=1)
        self.create_line(radius, height / 2, width - radius, height / 2, fill=c.LIGHT_BORDER, width=1)
        
        self.pair_1 = []
        self.pair_2 = []
        players = get_players_for_fixture(fixture_id)
        for p in players:
            if p["pair_number"] == 1:
                self.pair_1.append(p)
            else:
                self.pair_2.append(p)
                
        self._build_cell(self.pair_1, 0, width / 4, height / 4, bg_colour)
        self._build_cell(self.pair_1, 1, (width / 4) * 3, height / 4, bg_colour)
        self._build_cell(self.pair_2, 0, width / 4, (height / 4) * 3, bg_colour)
        self._build_cell(self.pair_2, 1, (width / 4) * 3, (height / 4) * 3, bg_colour)
        
    #Method to build a single name label inside one quadrant of the table
    def _build_cell(self, pair, col_index, x, y, bg_colour):
        if col_index < len(pair):
            player = pair[col_index]
            name = f"{player['firstname']} {player['surname']}"
        else:
            name = "TBC"

        lbl = tk.Label(self, text=name, font=c.FONT_LABEL, bg=bg_colour, fg=c.LIGHT_MAIN_TEXT)
        self.create_window(x, y, window=lbl)