import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item

#Class that can be imported to add a frame of cards for fixtures onto the screen
class fixture_cards(tk.Frame):
    def __init__(self, parent, fixtures, want_colour_change_background, on_click):
        super().__init__(parent, background=c.LIGHT_BACKGROUND)
        self.pack(fill="x")
        
        self.on_click = on_click
        
        #Loop to go through every fixture and create its card
        for fixture in fixtures:
            if (want_colour_change_background):
                if fixture["is_selected"] == True:
                    self.create_card_frame(fixture, c.LIGHT_SUCCESS, c.LIGHT_SUCCESS_HOVER)
                else:
                    self.create_card_frame(fixture, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
            else:
                self.create_card_frame(fixture, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
            
    
    #Method to create a fixture card            
    def create_card_frame(self, fixture, bg_colour, hover_colour):
        top_sentence = f"{fixture['opposition']} ({fixture['home_away']})"
        bottom_sentence = f"Date: {fixture['date']}"
        
        card = Rounded_Item(self, width=500, height=70, radius=16, bg_colour=bg_colour, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=hover_colour, command=lambda f=fixture: self.on_click(f))
        card.pack(padx=10, pady=5)
        
        lbl_top = tk.Label(card.content, text=top_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_top.pack()
        
        lbl_bottom = tk.Label(card.content, text=bottom_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_bottom.pack()
        
        #Include the labels added after the rounded item was constructed.
        card.bind_children()
