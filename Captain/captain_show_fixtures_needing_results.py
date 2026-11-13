import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.fixture_cards import fixture_cards
from SQL import get_fixtures_without_results
import tkinter as tk


class Captain_Show_Fixtures_Needing_Results(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create label for fixtures
        self.lbl_fixtures = tk.Label(self, text="Fixtures Needing Results", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_fixtures.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put fixture cards onto the screen
        self.fixtures = get_fixtures_without_results(self.user_id)
        self.fixture_frame = fixture_cards(self, self.fixtures, False, self.open_add_result)
        self.fixture_frame.pack()
        
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_manage_fixtures, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to open the add result screen
    def open_add_result(self, fixture):
        self.app.show_add_or_edit_result_screen(self.user_id, True, fixture["fixture_id"])
        
        
    #Method to return to the manage fixtures screen
    def return_to_manage_fixtures(self):
        self.app.show_manage_fixtures_screen(self.user_id)