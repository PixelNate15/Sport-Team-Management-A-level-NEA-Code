import constants as c
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.view_result_information_captain import View_Result_Details
from Reusable_Code.results_table import Result_Table, calculate_match_totals
from System.form_score_calculation import calculate_form_score
from SQL.fixtures import get_players_for_fixture
from SQL.results import get_result, get_matches_for_fixture, save_match
import tkinter as tk
from tkinter import messagebox


class Captain_Add_Or_Edit_Result(tk.Frame):
    def __init__(self, parent, app, user_id, is_new, fixture_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.is_new = is_new
        self.fixture_id = fixture_id
        
        #Puts the title on the screen
        self.title_text = "Add Result" if is_new else "Edit Result"
        self.title = tk.Label(self, text=self.title_text, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put the result details on the screen
        self.result_details_info = get_result(self.fixture_id)
        self.fixture_date = self.result_details_info["date"]
        self.result_details = View_Result_Details(self, self.result_details_info)
        self.result_details.pack(side="top", fill="x")
        
        #Gets the saved matches if the result is being edited, an empty list is used if nothing could be retrieved
        self.saved_matches = [] if self.is_new else (get_matches_for_fixture(self.fixture_id) or [])
        
        #Works out the message to show if the grid cannot be shown
        self.players = self.make_pairings()
        self.error_message = None
        if not self.players:
            self.error_message = "A full team must be selected for this fixture before a result can be added"
        elif not self.is_new and len(self.saved_matches) != 4:
            self.error_message = "The saved result for this fixture is incomplete and cannot be edited"
        
        if self.error_message is None:
            #Puts the score grid on the screen
            self.score_grid = Result_Table(self, self.players)
            self.score_grid.pack(pady=10)
            
            #If the result is being edited, the saved scores are put into the grid
            if not self.is_new:
                self.populate_scores()
            
            #Put submit button onto the screen
            self.btn_submit = Rounded_Item(self, text="Submit Result", command=self.submit_result, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit.pack(pady=15)
        else:
            #Shows the message instead of the grid
            self.lbl_error = tk.Label(self, text=self.error_message, font=c.FONT_LABEL, fg=c.LIGHT_ERROR, bg=c.LIGHT_BACKGROUND)
            self.lbl_error.pack(pady=20)
        
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_previous_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        self.app.scrollable_frame.bind_children()
        
        
    #Method to make the four matches from the team selected for the fixture
    def make_pairings(self):
        selected_players = get_players_for_fixture(self.fixture_id)
        if not selected_players or len(selected_players) < 4:
            self.match_setup = None
            return None
        
        p1, p2, p3, p4 = selected_players[:4]
        
        pairings = [(p1, p2), (p3, p4), (p1, p2), (p3, p4)]
        pair_numbers = [1, 2, 1, 2]
        opponent_pair_numbers = [1, 2, 2, 1]
        
        self.match_setup = []
        names = []
        for index, (first, second) in enumerate(pairings):
            names.append(f"{first['firstname']} {first['surname']} / {second['firstname']} {second['surname']}")
            self.match_setup.append({
                "players": (first["user_id"], second["user_id"]),
                "pair_number": pair_numbers[index],
                "opponent_pair_number": opponent_pair_numbers[index]
            })
        return names
    
    
    #Method to put the saved scores into the grid, the saved matches are in the same order as the grid rows
    def populate_scores(self):
        for row, saved in zip(self.score_grid.scores, self.saved_matches):
            values = [saved["set_1_won"], saved["set_1_lost"], saved["set_2_won"], saved["set_2_lost"]]
            for variable, value in zip(row["sets"], values):
                variable.set("" if value is None else str(value))
            row["champ_tie"].set(saved["champ_tie"] if saved["champ_tie"] else "None")
    
    
    #Method to build the list of match dictionaries from the grid, returns None if any row is invalid
    def build_matches(self):
        matches = []
        for index, (row, setup) in enumerate(zip(self.score_grid.get_scores(), self.match_setup)):
            totals, error = calculate_match_totals(row)
            if error:
                messagebox.showinfo(message=error, title="Result Error")
                return None
            
            player_1, player_2 = setup["players"]
            matches.append({
                "match_id": None if self.is_new else self.saved_matches[index]["match_id"],
                "pair_number": setup["pair_number"],
                "opponent_pair_number": setup["opponent_pair_number"],
                "player_1": player_1,
                "player_2": player_2,
                "form_1": calculate_form_score(player_1, self.fixture_date),
                "form_2": calculate_form_score(player_2, self.fixture_date),
                **totals
            })
        return matches
    
    
    #Method to validate the scores and then add or update each match of the result
    def submit_result(self):
        self.matches = self.build_matches()
        if self.matches is None:
            return
        
        #Each match is saved one at a time
        for match in self.matches:
            if not save_match(self.fixture_id, self.fixture_date, match, self.is_new):
                messagebox.showinfo(message="The result could not be saved, please try again", title="Result Error")
                
                if self.is_new:
                    self.return_to_previous_screen()
                return
        
        messagebox.showinfo(message="Result Added" if self.is_new else "Result Updated", title="Result")
        self.return_to_previous_screen()
    
    
    #Method to return to the screen the captain came from
    def return_to_previous_screen(self):
        if self.is_new:
            self.app.show_fixtures_needing_results(self.user_id)
        else:
            self.app.show_manage_fixtures_screen(self.user_id)
