import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.fixture_cards import fixture_cards
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
import tkinter as tk

class Member_Availability_Screen(tk.Frame):
    def __init__(self, parent, app, user_id, fixtures):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.fixtures = fixtures
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create the title for the page using a label
        self.lbl_Title = tk.Label(self, text="Availability", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="left")
        self.lbl_Title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Create the fixture cards
        self.fixture_frame = fixture_cards(self, self.fixtures, False, self.open_select_availbility)
        self.fixture_frame.pack()
        
        #Add button to bottom of screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_login_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to open the select availbility screen
    def open_select_availbility(self, fixture):
        self.app.show_member_select_availability_screen(self.user_id, fixture, self.fixtures)
        

    #Method to return to login screen
    def return_to_login_screen(self):
        self.app.show_main_screen(self.user_id)