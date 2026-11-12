import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.time_entry import Time_Entry
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from System.generate_recommended_team import generate_recommended_team
from SQL import get_fixture_information, get_players_in_one_squad, get_players_for_fixture, insert_fixture, update_fixture
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry

class Captain_Add_Or_Edit_Fixture(tk.Frame):
    def __init__(self, parent, app, user_id, is_new, fixture_id=None):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.is_new = is_new
        self.fixture_id = fixture_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Puts the title on the screen
        self.title_text = "Add Fixture" if is_new else "Edit Fixture"
        self.title = tk.Label(self, text=self.title_text, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.title.pack(anchor="w", padx=(10,0), pady=10)
                
        
        #-- Puts the fixture detail widgets on the screen --#
        
        #Creates the Opponent Name widgets
        self.lbl_opponent_name = tk.Label(self, text="Opponent Name:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_opponent_name.pack()
        self.ent_opponent_name = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=50)
        self.ent_opponent_name.pack(pady=(0,5))
        
        #Create the Date widgets
        self.lbl_date = tk.Label(self, text="Date:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_date.pack()
        self.ent_date = DateEntry(self, width=15, date_pattern="dd/mm/yyyy")
        self.ent_date.pack(pady=(0,10))
        
        #Create the Start Time widgets
        self.lbl_start_time = tk.Label(self, text="Start Time:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_start_time.pack()
        self.time_entry = Time_Entry(self)
        self.time_entry.pack(padx=10, pady=10)
        
        #Create the Location widgets
        self.lbl_location = tk.Label(self, text="Location:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_location.pack()
        self.ent_location = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=50)
        self.ent_location.pack(pady=(0,5))
        
        #Create the Is Home widgets
        self.lbl_can_you_play = tk.Label(self, text="Is At Home?:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_can_you_play.pack()
        self.can_play = IntVar(value=1)
        self.bx_can_play = Checkbutton(self, variable=self.can_play, onvalue=1, offvalue=0, height=0, width=0, bg=c.LIGHT_BACKGROUND, font=c.FONT_LABEL, activebackground=c.LIGHT_BACKGROUND)
        self.bx_can_play.pack()
        
        #Create the Opponent league Position widgets
        self.lbl_opponent_league_position = tk.Label(self, text="Opponent League Position:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_opponent_league_position.pack()
        self.ent_opponent_league_position = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=50)
        self.ent_opponent_league_position.pack(pady=(0,5))
        
        #Creates the Notes widgets
        self.lbl_notes = tk.Label(self, text="Notes:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_notes.pack()
        self.txt_notes = tk.Text(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, width=50, height=6)
        self.txt_notes.pack()
        
        
        #-- Puts the player details onto the screen --#
        
        #Create the grid
        self.input_players_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.input_players_frame.pack(padx=15, pady=(30,10))
        
        #Configure the frame into three columns
        self.input_players_frame.grid_columnconfigure(0, weight=1, uniform="player_entries")
        self.input_players_frame.grid_columnconfigure(1, weight=0)
        self.input_players_frame.grid_columnconfigure(2, weight=1, uniform="player_entries")
        
        #Configure the frame so the row with scrollable frames can expand
        self.input_players_frame.grid_rowconfigure(1, weight=1)
        
        #Create the title labels
        self.lbl_recommended = tk.Label(self.input_players_frame, text="Recommended Team (ONLY AN AID)", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_recommended.grid(row=0, column=0, pady=10)
        
        self.lbl_players = tk.Label(self.input_players_frame, text="Players for Match", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_players.grid(row=0, column=2, pady=10)
        
        #Creates the divider across the middle
        self.middle_divider = tk.Frame(self.input_players_frame, bg=c.LIGHT_MAIN_TEXT, width=2)
        self.middle_divider.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10)
        
        #Creates the divider across the bottom of the frames
        self.bottom_divider = tk.Frame(self.input_players_frame, bg=c.LIGHT_MAIN_TEXT, width=2)
        self.bottom_divider.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        #Creates the main content of the screen
        self.recommended_frame = tk.Frame(self.input_players_frame, bg=c.LIGHT_BACKGROUND)
        self.recommended_frame.grid(row=1, column=0, padx=15, pady=10)
        
        self.players_frame = tk.Frame(self.input_players_frame, bg=c.LIGHT_BACKGROUND)
        self.players_frame.grid(row=1, column=2, padx=15, pady=10)
        
        
        #-- Creates the player frame for the recommended team --#
        
        #Player and entry widget creation for player 1
        self.lbl_rec_p1 = tk.Label(self.recommended_frame, text="Player 1:", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_rec_p1.grid(row=0, column=0, pady=10)
        self.ent_rec_p1 = tk.Entry(self.recommended_frame, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", state="readonly")
        self.ent_rec_p1.grid(row=0, column=1, sticky="w", padx=(10,0))
        
        #Player and entry widget creation for player 2
        self.lbl_rec_p2 = tk.Label(self.recommended_frame, text="Player 2:", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_rec_p2.grid(row=1, column=0, pady=10)
        self.ent_rec_p2 = tk.Entry(self.recommended_frame, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", state="readonly")
        self.ent_rec_p2.grid(row=1, column=1, sticky="w", padx=(10,0))
        
        #Player and entry widget creation for player 3
        self.lbl_rec_p3 = tk.Label(self.recommended_frame, text="Player 3:", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_rec_p3.grid(row=2, column=0, pady=10)
        self.ent_rec_p3 = tk.Entry(self.recommended_frame, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", state="readonly")
        self.ent_rec_p3.grid(row=2, column=1, sticky="w", padx=(10,0))
        
        #Player and entry widget creation for player 4
        self.lbl_rec_p4 = tk.Label(self.recommended_frame, text="Player 4:", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_rec_p4.grid(row=3, column=0, pady=10)
        self.ent_rec_p4 = tk.Entry(self.recommended_frame, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", state="readonly")
        self.ent_rec_p4.grid(row=3, column=1, sticky="w", padx=(10,0))
        
        
        #-- Creates the player dropdowns for the captains team --#
        
        #Styles the dropdowns so they match the entries on the rest of the screen
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Player.TCombobox", fieldbackground=c.LIGHT_SIDEBAR, background=c.LIGHT_SIDEBAR, foreground=c.LIGHT_PRIMARY_ACCENT, arrowcolor=c.LIGHT_MAIN_TEXT, bordercolor=c.LIGHT_BORDER, lightcolor=c.LIGHT_SIDEBAR, darkcolor=c.LIGHT_SIDEBAR, selectbackground=c.LIGHT_SIDEBAR, selectforeground=c.LIGHT_PRIMARY_ACCENT)
        self.style.map("Player.TCombobox", fieldbackground=[("readonly", c.LIGHT_SIDEBAR)], foreground=[("readonly", c.LIGHT_PRIMARY_ACCENT)])
        
        #Styles the list that drops down when a dropdown is opened
        self.option_add("*TCombobox*Listbox.background", c.LIGHT_SIDEBAR)
        self.option_add("*TCombobox*Listbox.foreground", c.LIGHT_MAIN_TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", c.LIGHT_PRIMARY_ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", "white")
        self.option_add("*TCombobox*Listbox.font", c.FONT_ENTRY)
        
        #Gets all the players in the captains squad and creates a list of their names for the dropdowns
        self.squad_players = get_players_in_one_squad(self.user_id)
        self.player_names = []
        for player in self.squad_players:
            self.player_names.append(f"{player['firstname']} {player['surname']}")
        
        #Loop creating the label and dropdown for each of the 4 player spots
        self.cap_dropdowns = []
        for i in range(4):
            self.lbl_cap_player = tk.Label(self.players_frame, text=f"Player {i + 1}:", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
            self.lbl_cap_player.grid(row=i, column=0, pady=10)
            self.cmb_cap_player = ttk.Combobox(self.players_frame, values=self.player_names, state="readonly", style="Player.TCombobox", font=c.FONT_ENTRY, justify="center", width=20)
            self.cmb_cap_player.grid(row=i, column=1, sticky="w", padx=(10,0))
            self.cap_dropdowns.append(self.cmb_cap_player)
        
        self.recommended_team = None
        self.populate_widgets()
        
        if self.recommended_team:
            #Creates the frame which will hold the submit buttons at the bottom of the screen
            self.button_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
            self.button_frame.pack(padx=15, pady=10)
                    
            #Creates the submit with the recommended team button
            self.btn_submit_recommended = Rounded_Item(self.button_frame, text="Submit with Recommended Team", command=self.submit_with_recommended, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit_recommended.grid(row=0, column=0, padx=15)
            
            #Creates the submit with the captains team button
            self.btn_submit_captain = Rounded_Item(self.button_frame, text="Submit with Your Team", command=self.submit_with_captains, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit_captain.grid(row=0, column=1, padx=15)
        else:
            #Creates the submit with the captains team button
            self.btn_submit_captain = Rounded_Item(self, text="Submit with Your Team", command=self.submit_with_captains, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit_captain.pack(pady=15)
        
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_manage_fixtures, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to put text into a readonly entry
    def set_readonly_entry(self, entry, text):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state="readonly")
        
        
    #Method to select a player in a dropdown from their user_id
    def set_dropdown_player(self, dropdown, player_id):
        for index, squad_player in enumerate(self.squad_players):
            if squad_player["user_id"] == player_id:
                dropdown.current(index)
                return
        
        
    #Method to populate the widgets with information
    def populate_widgets(self):
        if self.is_new == False:
            self.fixture_information = get_fixture_information(self.fixture_id)
            self.existing_players = get_players_for_fixture(self.fixture_id)
            self.recommended_team = generate_recommended_team(self.fixture_id)
            
            #Insert fixture details
            self.ent_opponent_name.insert(0, self.fixture_information["opponent_name"])
            self.ent_date.set_date(self.fixture_information["date"])
            self.time_entry.set_time(self.fixture_information["start_time"])
            self.ent_location.insert(0, self.fixture_information["location"])
            self.can_play.set(1 if self.fixture_information["is_home"] else 0)
            if self.fixture_information["opponent_league_position"] is not None:
                self.ent_opponent_league_position.insert(0, self.fixture_information["opponent_league_position"])
            if self.fixture_information["notes"]:
                self.txt_notes.insert("1.0", self.fixture_information["notes"])
                
            #Insert recommended team entries
            if self.recommended_team:
                self.recommended_players = []
                for pair in self.recommended_team:
                    self.recommended_players.extend(pair)
                
                self.recommended_entries = [self.ent_rec_p1, self.ent_rec_p2, self.ent_rec_p3, self.ent_rec_p4]
                for entry, player in zip(self.recommended_entries, self.recommended_players):
                    self.set_readonly_entry(entry, f"{player['firstname']} {player['surname']}")
                    
            #Insert captains team dropdowns
            if self.existing_players:
                for i, existing_player in enumerate(self.existing_players[:4]):
                    self.set_dropdown_player(self.cap_dropdowns[i], existing_player["user_id"])
                    
        
        
    #Method to turn a list of user_ids into the list of player dictionaries the SQL functions need
    def create_players_list(self, user_ids):
        players = []
        for i, player_id in enumerate(user_ids):
            players.append({
                "user_id": player_id,
                "pair_number": 1 if i < 2 else 2,
                "selection_order": (i % 2) + 1
            })
        return players
    
    
    #Method to get the user_ids of the recommended team as a list
    def get_recommended_ids(self):
        if not self.recommended_team:
            return None
        
        recommended_ids = []
        for pair in self.recommended_team:
            for player in pair:
                recommended_ids.append(player["user_id"])
        
        if len(recommended_ids) != 4:
            return None
        return recommended_ids
    
    
    #Method to get the players chosen in the dropdowns as a list
    def get_captains_players(self):
        chosen_ids = []
        for dropdown in self.cap_dropdowns:
            index = dropdown.current()
            if index == -1:
                messagebox.showinfo(message="Please select a player for every spot", title="Team Selection Error")
                return None
            chosen_ids.append(self.squad_players[index]["user_id"])
        
        #Checks that the same player has not been picked more than once
        if len(set(chosen_ids)) != len(chosen_ids):
            messagebox.showinfo(message="A player cannot be selected more than once", title="Team Selection Error")
            return None
        
        return self.create_players_list(chosen_ids)
    
    
    #Method to get the recommended team as a list
    def get_recommended_players(self):
        recommended_ids = self.get_recommended_ids()
        if recommended_ids is None:
            messagebox.showinfo(message="There is no full recommended team available for this fixture", title="Team Selection Error")
            return None
        return self.create_players_list(recommended_ids)
    
    
    #Method to submit with the recommended team
    def submit_with_recommended(self):
        self.players = self.get_recommended_players()
        if self.players is None:
            return
        self.submit(self.players)
    
    
    #Method to submit with the captains team
    def submit_with_captains(self):
        self.players = self.get_captains_players()
        if self.players is None:
            return
        self.submit(self.players)
    
    
    #Method to validate the fixture details and then add or update the fixture with the players given
    def submit(self, players):
        self.opponent_name = self.ent_opponent_name.get().strip()
        self.fixture_date = self.ent_date.get_date()
        self.start_time = self.time_entry.get_time()
        self.location = self.ent_location.get().strip()
        self.is_home = self.can_play.get() == 1
        self.league_position = self.ent_opponent_league_position.get().strip()
        self.notes = self.txt_notes.get("1.0", tk.END).strip()
        
        #Validation for opponent name
        if not self.opponent_name:
            messagebox.showinfo(message="Please enter the opponent name", title="Fixture Error")
            return
        elif len(self.opponent_name) > 50:
            messagebox.showinfo(message="Opponent name is too long", title="Fixture Error")
            return
        
        #Validation for start time
        if self.start_time is None:
            messagebox.showinfo(message="Please enter a valid start time", title="Fixture Error")
            return
        
        #Validation for location
        if not self.location:
            messagebox.showinfo(message="Please enter the location", title="Fixture Error")
            return
        elif len(self.location) > 20:
            messagebox.showinfo(message="Location is too long", title="Fixture Error")
            return
        
        #Validation for opponent league position, it is optional so empty becomes None
        if self.league_position == "":
            messagebox.showinfo(message="League position must entered", title="Fixture Error")
        elif self.league_position.isdigit() and int(self.league_position) > 0:
            self.league_position = int(self.league_position)
        else:
            messagebox.showinfo(message="League position must be a whole number above 0", title="Fixture Error")
            return
        
        #Notes are optional so empty becomes None
        if not self.notes:
            self.notes = None
        
        if self.is_new:
            self.new_fixture_id = insert_fixture(self.user_id, self.opponent_name, self.fixture_date, self.start_time, self.location, self.is_home, self.league_position, self.notes, players)
            if self.new_fixture_id is None:
                messagebox.showinfo(message="The fixture could not be added", title="Fixture Error")
                return
            messagebox.showinfo(message="Fixture Added", title="Fixture")
        else:
            update_fixture(self.fixture_id, self.opponent_name, self.fixture_date, self.start_time, self.location, self.is_home, self.league_position, self.notes, players)
            messagebox.showinfo(message="Fixture Updated", title="Fixture")
        
        self.return_to_manage_fixtures()
    
    
    #Method to return to the manage fixture screen
    def return_to_manage_fixtures(self):
        self.app.show_manage_fixtures_screen(self.user_id)