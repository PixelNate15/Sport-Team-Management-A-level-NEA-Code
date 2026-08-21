import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_cards import Rounded_Card


class player_cards(tk.Frame):
    def __init__(self, parent, players, on_click):
        super().__init__(parent, background=c.LIGHT_BACKGROUND)
        self.pack(fill="x")
        
        self.on_click = on_click
        
        #Loop through every player and create a card for each
        for player in players:
            self.create_card_frame(player, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
            
    
    #Method to create a fixture card            
    def create_card_frame(self, player, bg_colour, hover_colour):
        initials = f"{player["firstname"][0]}{player["surname"][0]}".upper()
        name_sentence = f"{player["firstname"]} {player["surname"]}"
        rows = [
            ("Games Played:", player["games_played"]),
            ("Win Percentage:", f"{player["win_percentage"]}%")
        ]
        
        card = Rounded_Card(self, width=500, height=70, radius=16, bg_colour=bg_colour, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=hover_colour)
        card.pack(fill="x", padx=10, pady=5)
        
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
        
        #Bind click and hover to whole card, recursively doing it to all child widgets
        self.bind_click(card, lambda p=player: self.on_click(p))
        self.bind_hover(card, card.bg_colour, card.hover_colour)
            
        
    #Method to give a card the ability to be clicked 
    def bind_click(self, widget, command):
        widget.bind("<Button-1>", lambda e: command())
        for child in widget.winfo_children():
            self.bind_click(child, command)
            
    
    #Method to changed the bg colour of a card when its being hovered over
    def bind_hover(self, card, bg_colour, hover_colour):

        def on_enter(event):
            card.set_colour(hover_colour)

        def on_leave(event):
            # Find the widget currently underneath the mouse
            widget_under_mouse = card.winfo_containing(
                card.winfo_pointerx(),
                card.winfo_pointery()
            )

            # Only remove hover if we've actually left the whole card
            widget = widget_under_mouse

            while widget is not None:
                if widget == card:
                    return
                try:
                    widget = widget.master
                except:
                    break
            card.set_colour(bg_colour)

        def bind_recursive(widget):
            widget.bind("<Enter>", on_enter, add="+")
            widget.bind("<Leave>", on_leave, add="+")

            for child in widget.winfo_children():
                bind_recursive(child)

        bind_recursive(card)