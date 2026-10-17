import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item


class player_cards(tk.Frame):
    def __init__(self, parent, players, on_click, want_grid=False):
        super().__init__(parent, background=c.LIGHT_BACKGROUND)
        
        self.on_click = on_click
        self.want_grid = want_grid
        
        if self.want_grid:
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
                   
        #Loop through every player and create a card for each
        for i, player in enumerate(players):
            if self.want_grid == True:
                row = i // 2
                column = i % 2
            else:
                row = None
                column = None
            self.create_card_frame(player, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER, row, column)
            
    
    #Method to create a fixture card         
    def create_card_frame(self, player, bg_colour, hover_colour, row=None, column=None):
        initials = f"{player["firstname"][0]}{player["surname"][0]}".upper()
        name_sentence = f"{player["firstname"]} {player["surname"]}"
        rows = [
            ("Games Played:", player["games_played"]),
            ("Win Percentage:", f"{player["win_percentage"]}%")
        ]
        
        card = Rounded_Item(self, width=500, height=70, radius=16, bg_colour=bg_colour, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=hover_colour, command=lambda p=player: self.on_click(p))
        if self.want_grid == True:
            card.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
        else:    
            card.pack(padx=10, pady=5)
        
        #Circle avatar, sized to fill the card height with a small margin
        avatar_size = 54
        avatar_canvas = tk.Canvas(card.content, width=avatar_size, height=avatar_size, bg=bg_colour, highlightthickness=0)
        avatar_canvas.pack(side="left", padx=(10, 15))
        avatar_canvas.create_oval(2, 2, avatar_size - 2, avatar_size - 2, outline=c.LIGHT_MAIN_TEXT, width=2, fill=bg_colour, tags="avatar_background")
        avatar_canvas.create_text(avatar_size / 2, avatar_size / 2, text=initials, font=c.FONT_HEADING, fill=c.LIGHT_MAIN_TEXT)
        
        #Create label for name
        lbl_name = tk.Label(card.content, text=name_sentence, font=c.FONT_SUBHEADING, bg=bg_colour, fg="black")
        lbl_name.pack(side="left")
        
        stats_frame = tk.Frame(card.content, bg=bg_colour)
        stats_frame.pack(side="right", padx=(20, 0))

        for title, value in rows:
            lbl_stat = tk.Label(stats_frame, text=f"{title} {value}", font=c.FONT_LABEL, bg=bg_colour, fg=c.LIGHT_MAIN_TEXT, anchor="w")
            lbl_stat.pack(anchor="w")
        
        #Include the widgets added after the rounded item was constructed.
        card.bind_children()
