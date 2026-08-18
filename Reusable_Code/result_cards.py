import tkinter as tk
import constants as c
from Reusable_Code.Rounded_Items.rounded_cards import Rounded_Card
from SQL import has_submitted_feedback


#Class that can be imported to add a frame of cards for fixture results onto the screen
class result_cards(tk.Frame):
    def __init__(self, parent, results, on_click, for_feedback, user_id = None):
        super().__init__(parent, background=c.LIGHT_BACKGROUND)
        self.pack(fill="x")
        
        self.on_click = on_click
        self.for_feedback = for_feedback
        self.user_id = user_id
        
        #Loop to go through every fixture and create its card
        for result in results:
            if self.for_feedback == False:
                if result["did_win"]:
                    self.create_card_frame(result, c.LIGHT_SUCCESS, c.LIGHT_SUCCESS_HOVER)
                else:
                    if result["sets_won"] == result["sets_lost"]:
                        self.create_card_frame(result, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
                    else:
                        self.create_card_frame(result, c.LIGHT_ERROR, c.LIGHT_ERROR_HOVER)
            else:
                if not has_submitted_feedback(result["fixture_id"], self.user_id):
                    self.create_card_frame(result, c.LIGHT_SIDEBAR, c.LIGHT_SIDEBAR_HOVER)
                
    #Method to create a result card
    def create_card_frame(self, result, bg_colour, hover_colour):
        top_sentence = f"Result: {result['sets_won']} - {result['sets_lost']}"
        middle_sentence = f"{result['opposition']} ({result['home_away']})"
        bottom_sentence = f"Date: {result['date']}"
        
        card = Rounded_Card(self, width=500, height=70, radius=16, bg_colour=bg_colour, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=hover_colour)
        card.pack(fill="x", padx=10, pady=5)
        
        lbl_top = tk.Label(card.content, text=top_sentence, font=c.FONT_LABEL_BOLD, bg=bg_colour, fg="black")
        lbl_top.pack()
        
        lbl_middle = tk.Label(card.content, text=middle_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_middle.pack()
        
        lbl_bottom = tk.Label(card.content, text=bottom_sentence, font=c.FONT_LABEL, bg=bg_colour, fg="black")
        lbl_bottom.pack()
        
        #Bind click and hover to whole card, recursively doing it to all child widgets
        self.bind_click(card, lambda f=result: self.on_click(f))
        self.bind_hover(card, card.bg_colour, card.hover_colour)
            
        
    
    #Method to give a card the ability to be clicked 
    def bind_click(self, widget, command):
        widget.bind("<Button-1>", lambda e: command())
        for child in widget.winfo_children():
            self.bind_click(child, command)
            
    
    #Method to changed the bg colour of a card when its being hovered over
    def bind_hover(self, card, bg_colour, hover_colour):
        card.canvas.bind("<Enter>", lambda e: card.set_colour(hover_colour))
        card.canvas.bind("<Leave>", lambda e: card.set_colour(bg_colour))