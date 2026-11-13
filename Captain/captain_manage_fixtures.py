import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.scrollable_frame import Scrollable_Frame
from Reusable_Code.fixture_cards import fixture_cards
from Reusable_Code.result_cards import result_cards
from SQL import get_squad_upcoming_fixtures, get_squad_results, remove_fixture
import tkinter as tk
from tkinter import messagebox

class Captain_Manage_Fixtures(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.remove_fixture_selection = False
        self.selected_fixtures = []
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Creates the main frame to hold both columns in
        self.main_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=10)
               
        #Configure the frame into three columns
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="fixture_columns")
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1, uniform="fixture_columns")
        
        #Configure the frame so the row with scrollable frames can expand
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        #Create the title labels
        self.lbl_upcoming = tk.Label(self.main_frame, text="Upcoming Fixtures", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_upcoming.grid(row=0, column=0, pady=10)
        
        self.lbl_results = tk.Label(self.main_frame, text="Results", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_results.grid(row=0, column=2, pady=10)
        
        #Creates the divider across the middle
        self.middle_divider = tk.Frame(self.main_frame, bg=c.LIGHT_MAIN_TEXT, width=2)
        self.middle_divider.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10)
        
        #Creates the divider across the bottom of the frames
        self.bottom_divider = tk.Frame(self.main_frame, bg=c.LIGHT_MAIN_TEXT, width=2)
        self.bottom_divider.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        #Creates the scrollable frames
        self.upcoming_scroll = Scrollable_Frame(self.main_frame, width=540, height=200)
        self.upcoming_scroll.grid(row=1, column=0, sticky="nsew", padx=5)

        self.results_scroll = Scrollable_Frame(self.main_frame, width=540, height=200)
        self.results_scroll.grid(row=1, column=2, sticky="nsew", padx=5)
        
        #Gets the fixtures/results
        self.upcoming_fixtures = get_squad_upcoming_fixtures(self.user_id)
        self.results = get_squad_results(self.user_id)
        
        #Fills the frames with data
        if self.upcoming_fixtures:
            self.fixture_frame = fixture_cards(self.upcoming_scroll.content, self.upcoming_fixtures, False, self.expand_fixture_card)
        else:
            self.lbl_no_upcoming = tk.Label(self.upcoming_scroll.content, text="No upcoming fixtures", font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
            self.lbl_no_upcoming.pack(pady=20)
        
        if self.results:
            self.result_cards = result_cards(self.results_scroll.content, self.results, self.expand_result_card, False)
        else:
            #Display a message if there are no completed fixtures
            self.lbl_no_results = tk.Label(self.results_scroll.content, text="No results available", font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
            self.lbl_no_results.pack(pady=20)

        #Bind mouse wheel scrolling after all cards have been created
        self.upcoming_scroll.bind_children()
        self.results_scroll.bind_children()
        
        #Creates the button frame to hold all the buttons
        self.button_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.button_frame.pack(padx=15, pady=10)
        
        #-- Creates the buttons to go into the frame --#
        
        #Creats the add fixture button
        self.btn_add_fixture = Rounded_Item(self.button_frame, text="Add Fixture", command=self.add_new_fixture, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_add_fixture.grid(row=0, column=0, padx=15)
        
        #Creats the remove fixture button
        self.btn_remove_fixture_selecetion = Rounded_Item(self.button_frame, text="Remove Fixture Selection", command=self.select_remove_fixtures, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_remove_fixture_selecetion.grid(row=0, column=1, padx=15)
        
        #Creats the add result button
        self.btn_add_result = Rounded_Item(self.button_frame, text="Add Result", command=self.open_add_result_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_add_result.grid(row=0, column=2, padx=15)
        
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
      
      
    #Method to return to the captain home screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)
        
        
    #Method to expand a fixture card
    def expand_fixture_card(self, fixture):
        self.app.show_add_or_edit_fixture_screen(self.user_id, False, fixture["fixture_id"])
    
    
    #Method to show the add new fixture screen
    def add_new_fixture(self):
        self.app.show_add_or_edit_fixture_screen(self.user_id, True)
    
    
    #Method to expand a result card
    def expand_result_card(self, fixture):
        self.app.show_add_or_edit_result_screen(self.user_id, False, fixture["fixture_id"])
    
    
    #Method to select fixtures to remove
    def select_remove_fixtures(self):
        self.remove_fixture_selection = not self.remove_fixture_selection
        if self.remove_fixture_selection:
            self.btn_submit = Rounded_Item(self, text="Submit Fixture Removal", command=self.remove_fixture, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit.pack(pady=15, before=self.btn_back)
        else:
            self.btn_submit.pack_forget()
        self.selected_fixtures = []
        self._draw_fixture_cards()
        
        
    #Method to select a fixture
    def select_fixture(self, fixture):
        fixture_id = fixture["fixture_id"]
        if fixture_id in self.selected_fixtures:
            self.selected_fixtures.remove(fixture_id)
            self.fixture_frame.change_colour(fixture_id, False)
        else:
            self.selected_fixtures.append(fixture_id)
            self.fixture_frame.change_colour(fixture_id, True)
        
        
    #Method to draw the fixture cards
    def _draw_fixture_cards(self):
        for widget in self.upcoming_scroll.content.winfo_children():
            widget.destroy()
        
        if self.upcoming_fixtures:
            on_click = self.select_fixture if self.remove_fixture_selection else self.expand_fixture_card
            self.fixture_frame = fixture_cards(self.upcoming_scroll.content, self.upcoming_fixtures, False, on_click, self.selected_fixtures)
        else:
            self.lbl_no_upcoming = tk.Label(self.upcoming_scroll.content, text="No upcoming fixtures", font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
            self.lbl_no_upcoming.pack(pady=20)
            
        self.upcoming_scroll.bind_children()
        
        
    #Method to submit fixtures to be removed
    def remove_fixture(self):
        for fixture_id in self.selected_fixtures:
            remove_fixture(fixture_id)
        messagebox.showinfo(message="Fixtures Removed", title="Remove Fixtures") if self.selected_fixtures else messagebox.showinfo(message="Cannot remove No fixtures", title="Remove Fixtures")
        self.selected_fixtures = []
        self.remove_fixture_selection = False
        self.upcoming_fixtures = get_squad_upcoming_fixtures(self.user_id)
        self.btn_submit.pack_forget()
        self._draw_fixture_cards()
    
    
    #Method to open the add new result screen
    def open_add_result_screen(self):
        self.app.show_fixtures_needing_results(self.user_id)
            