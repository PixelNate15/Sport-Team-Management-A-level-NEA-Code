import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.players_selected_for_fixture_table import Team_Selection_Table
from Reusable_Code.view_fixture_information import View_Fixture_Details
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
import tkinter as tk


class Member_Expanded_Fixture_Card_Screen(tk.Frame):
    def __init__(self, parent, app, user_id, fixture):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.fixture = fixture
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Put team selection table onto the screen
        self.selection_table = Team_Selection_Table(self, fixture["fixture_id"])
        self.selection_table.pack(pady=10)
        
        #Put the fixture details on the screen
        self.fixture_details = View_Fixture_Details(self, fixture)
        self.fixture_details.pack(side="top", fill="x")
        
        #Add button to bottom of screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_login_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to return to login screen
    def return_to_login_screen(self):
        self.app.show_main_screen(self.user_id)