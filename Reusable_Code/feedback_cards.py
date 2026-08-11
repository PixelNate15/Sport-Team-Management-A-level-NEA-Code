import constants as c
from Reusable_Code.Rounded_Items.rounded_cards import Rounded_Card
import tkinter as tk

class Feedback_Cards(tk.Frame):
    def __init__(self, parent, feedbacks):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.pack(fill="x")
        
        #Loop to go through every bit of feedback and create their card
        for feedback in feedbacks:
            self.create_card_frame(feedback)
            
            
    #Method to create a feedback card
    def create_card_frame(self, feedback):
        title_sentence = f"{feedback['opposition']} ({feedback['home_away']}) - {feedback['date']}"
        ratings_sentence = f"Overall: {feedback['overall_rating']}/10   Key Moments: {feedback['key_moments_rating']}/10   Communication: {feedback['communication_rating']}/10"
        
        card = Rounded_Card(self, width=500, height=80, radius=16, bg_colour=c.LIGHT_SIDEBAR, parent_bg_colour=c.LIGHT_BACKGROUND, hover_colour=None)
        card.pack(fill="x", padx=10, pady=5)
        
        lbl_title = tk.Label(card.content, text=title_sentence, font=c.FONT_LABEL, bg=c.LIGHT_SIDEBAR, fg="black")
        lbl_title.pack()
        
        lbl_ratings = tk.Label(card.content, text=ratings_sentence, font=c.FONT_LABEL, bg=c.LIGHT_SIDEBAR, fg="black")
        lbl_ratings.pack()
        
        lbl_comment = tk.Label(card.content, text=feedback["comments"], font=c.FONT_LABEL, bg=c.LIGHT_SIDEBAR, fg="black")
        lbl_comment.pack()