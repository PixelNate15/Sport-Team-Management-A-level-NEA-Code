import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.result_cards import result_cards
from SQL import get_result_of_fixture_for_one_user
import tkinter as tk


class Member_Show_Required_Partner_Feedback(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create label for results
        self.lbl_results = tk.Label(self, text="Feedback Required", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_results.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put result cards onto the screen
        self.results = get_result_of_fixture_for_one_user(self.user_id)
        self.results_frame = result_cards(self, self.results, self.submit_feedback, True, self.user_id)
        self.results_frame.pack()
        
        #Put back button onto the screen 
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to go to submit feedback screen
    def submit_feedback(self, result):
        self.app.show_submit_partner_feedback(self.user_id, result)
        

    #Method to return to login screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)