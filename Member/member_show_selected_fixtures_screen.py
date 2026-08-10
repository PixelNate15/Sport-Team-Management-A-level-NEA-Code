import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.fixture_cards import fixture_cards
import tkinter as tk


class Member_Show_Selected_Fixtures_Screen(tk.Frame):
    def __init__(self, parent, app, user_id, fixtures):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.fixtures = fixtures
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create label for fixtures
        self.lbl_fixtures = tk.Label(self, text="Selected Fixtures", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_fixtures.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put fixture cards onto the screen
        for fixture in self.fixtures:
            if fixture["is_selected"] == True:
                self.fixture_frame = fixture_cards(self, [fixture], False, self.expand_card)
                self.fixture_frame.pack()
                
        #Put back button onto the screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to expand fixture card to view more details
    def expand_card(self, fixture):
        self.app.show_expanded_fixture(self.user_id, fixture)
        
        
    #Method to return to login screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)