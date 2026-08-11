import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.result_cards import result_cards
from SQL import get_result_of_fixture_for_one_user
import tkinter as tk


class Member_Show_Recent_Results(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create label for fixtures
        self.lbl_fixtures = tk.Label(self, text="Recent Results", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_fixtures.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put result cards onto the screen
        self.results = get_result_of_fixture_for_one_user(self.user_id)
        self.results_frame = result_cards(self, self.results, self.expand_card)
        self.results_frame.pack()
        
        
    #Method to expand a result card
    def expand_card(self):
        pass
    