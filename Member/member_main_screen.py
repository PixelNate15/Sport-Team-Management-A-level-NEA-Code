import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.main_screen_sidebar import main_screen_sidebar
from Reusable_Code.fixture_cards import fixture_cards
from SQL import get_fixtures
import tkinter as tk

class Member_Main_Screen(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create buttons for sidebar
        self.buttons = [
            ("Manage Availability", self.open_availability),
            ("Manage Injury Status", self.open_injury_status),
            ("View Selected Fixture", self.open_selected_fixtures),
            ("Partner Feedback", self.open_partner_feedback),
            ("Open Recent Results", self.open_recent_results)
        ]
        #Put sidebar on screen
        self.sidebar = main_screen_sidebar(self, self.buttons)
        self.sidebar.pack(side="left", fill="y")
        
        #Create label for fixtures
        self.lbl_fixtures = tk.Label(self, text="Fixtures", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_fixtures.pack(anchor="w", padx=(10,0), pady=10)
        
        #Get list of fixtures
        self.fixtures = get_fixtures(self.user_id)
        self.fixture_frame = fixture_cards(self, self.fixtures, True, self.expand_card)
        self.fixture_frame.pack()
        
       
    #Method to open the availability screen and close the main screen    
    def open_availability(self):
        self.app.show_member_availability_screen(self.user_id, self.fixtures)
        
        
    #Method to expand fixture card to view more details
    def expand_card(self, fixture):
        self.app.show_expanded_fixture(self.user_id, fixture)

    def open_injury_status(self):
        pass

    def open_selected_fixtures(self):
        self.app.show_selected_fixtures(self.user_id, self.fixtures)

    def open_partner_feedback(self):
        pass

    def open_recent_results(self):
        pass