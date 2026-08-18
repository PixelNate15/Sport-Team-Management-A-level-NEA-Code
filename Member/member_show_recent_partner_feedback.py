import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.feedback_cards import Feedback_Cards
from SQL import get_recent_partner_feedback
import tkinter as tk


class Member_Recent_Partner_Feedback(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Label to put the partner feedback they recieved for that match
        self.lbl_partnerfeedback = tk.Label(self, text="Partner Feedback", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_partnerfeedback.pack(pady=(10,0))
        
        #Put partner feedback card onto the screen
        self.feedback = get_recent_partner_feedback(self.user_id)
        self.feedback_frame = Feedback_Cards(self, self.feedback)
        self.feedback_frame.pack()
        
        #Put back button onto the screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to return to the recent_results_screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)