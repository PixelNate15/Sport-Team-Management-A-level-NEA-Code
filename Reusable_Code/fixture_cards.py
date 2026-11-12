import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item

#Class that can be imported to add a frame of cards for fixtures onto the screen
class fixture_cards(tk.Frame):
    def __init__(self, parent, fixtures, want_colour_change_background, on_click, selected_ids=None):
        super().__init__(parent, background=c.LIGHT_BACKGROUND)
        self.pack(fill="x")
        
        self.on_click = on_click
        self.selected_ids = selected_ids if selected_ids is not None else []
        self.cards = {}
        
        #Loop to go through every fixture and create its card
        if (want_colour_change_background):    
            for fixture in fixtures:
                if fixture["is_selected"] == True:
                    self.create_card_frame(fixture, c.LIGHT_SUCCESS, c.LIGHT_SUCCESS_HOVER)
                else:
                    self.create_card_frame(fixture, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
        else:
            for fixture in fixtures:
                self.create_card_frame(fixture, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
            
    
    #Method to create a fixture card            
    def create_card_frame(self, fixture, bg_colour, hover_colour):
        top_sentence = f"{fixture['opposition']} ({fixture['home_away']})"
        bottom_sentence = f"Date: {fixture['date']}"
        
        card = Rounded_Item(self, width=500, height=70, radius=16, bg_colour=bg_colour, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=hover_colour, command=lambda f=fixture: self.on_click(f))
        card.pack(padx=10, pady=5)
        self.cards[fixture["fixture_id"]] = card
        
        lbl_top = tk.Label(card.content, text=top_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_top.pack()
        
        lbl_bottom = tk.Label(card.content, text=bottom_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_bottom.pack()
        
        #Includes the labels added after the rounded item was constructed
        card.bind_children()
        
        
    #Method to change the background of a card
    def change_colour(self, user_id, is_selected):
        card = self.cards.get(user_id)
        if card is None:
            return
        if is_selected:
            card.change_colour(c.LIGHT_ERROR, c.LIGHT_ERROR_HOVER)
        else:
            card.change_colour(c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
