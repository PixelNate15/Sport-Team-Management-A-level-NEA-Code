import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.player_cards import player_cards
from SQL import get_club_id, get_all_players_for_squads_below_ranking, add_player_to_squad
import tkinter as tk
from tkinter import messagebox


class Captain_Show_All_Players_Available_For_Squad(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.screen_state = "analysis"
        self.selected_players = []
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Put title on the screen
        self.title = tk.Label(self, text="Players Available For Squad Choice", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Create Filter Grid
        self.filter_grid = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.filter_grid.columnconfigure(0, weight=1)
        self.filter_grid.columnconfigure(1, weight=1)
        self.filter_grid.columnconfigure(2, weight=1)
        self.filter_grid.pack(pady=10)
        
        self.ent_search = tk.Entry(self.filter_grid, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_search.grid(row=0, column=0, padx=(0,10))
        self.btn_search = Rounded_Item(self.filter_grid, text="Search", command=self.filter_player_cards, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_search.grid(row=0, column=1, padx=(0,10))
        self.btn_reset_search = Rounded_Item(self.filter_grid, text="Reset Search", command=self.reset_search, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_reset_search.grid(row=0, column=2)
        
        #Create player cards for all players in the captains squad ranking and below rankings
        self.club_id = get_club_id(self.user_id)
        self.players = get_all_players_for_squads_below_ranking(self.user_id, self.club_id)
        self.player_frame = player_cards(self, self.players, self.expand_card, True)
        self.player_frame.pack(fill="both", expand=True)
                
        #Put toggle screen state button on the screen
        self.btn_toggle_state = Rounded_Item(self, text="Select Players", command=self.toggle_screen_state, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_toggle_state.pack(pady=15)      
                
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to filter player cards
    def filter_player_cards(self):
        self.search = self.ent_search.get().strip().split()
        if len(self.search) == 1:
            for player in self.players:
                if player["firstname"].lower() == self.search[0].lower() or player["surname"].lower() == self.search[0].lower():
                    self.player_list = [player]
                    self._draw(self.player_list)
                    return
            self.player_frame.destroy()
        elif len(self.search) == 2:
            for player in self.players:
                if player["firstname"].lower() == self.search[0].lower() and player["surname"].lower() == self.search[1].lower():
                    self.player_list = [player]
                    self._draw(self.player_list)
                    return
            self.player_frame.destroy()
        elif len(self.search) == 0:
            self._draw(self.players, True)
        else:
            self.player_frame.destroy()
            
            
    #Method to reset the search
    def reset_search(self):
        self._draw(self.players, True)
        self.ent_search.delete(0, "end")
            
            
    #Method that adds/removes the selected player to a list
    def select_player_cards(self, player):
        player_id = player["user_id"]
        if player_id in self.selected_players:
            self.selected_players.remove(player_id)
            self.player_frame.change_colour(player_id, False)
        else:
            self.selected_players.append(player_id)
            self.player_frame.change_colour(player_id, True)
        
                
    #Method to draw the cards
    def _draw(self, players, want_grid=None):
        self.player_frame.destroy()
        if self.screen_state == "analysis":
             self.player_frame = player_cards(self, players, self.expand_card, bool(want_grid))
        else:
            self.player_frame = player_cards(self, players, self.select_player_cards, bool(want_grid), self.selected_players)
        self.player_frame.pack(fill="both", expand=True, after=self.filter_grid)
            
    
    #Method to add the players to the captains squad
    def submit_players(self):
        for player_id in self.selected_players:
            add_player_to_squad(self.user_id, player_id)
        messagebox.showinfo(message="Players Added to Squad", title="Squad Additions") if self.selected_players else messagebox.showinfo(message="Cannot add No-one to the Squad", title="Squad Additions")
        self.selected_players = []
        self.players = get_all_players_for_squads_below_ranking(self.user_id, self.club_id)
        self._draw(self.players, True)
            
            
    #Method to toggle the screen state
    def toggle_screen_state(self):
        if self.screen_state == "analysis":
            self.screen_state = "select"
            self.btn_toggle_state.configure_button_text("Analyse Players")
            self._draw(self.players, True)
            self.ent_search.delete(0, "end")
            
            #Put submit button on the screen
            self.btn_submit = Rounded_Item(self, text="Submit", command=self.submit_players, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit.pack(pady=15, before=self.btn_toggle_state)
        
        else:
            self.screen_state = "analysis"
            self.btn_toggle_state.configure_button_text("Select Players")
            self._draw(self.players, True)
            self.btn_submit.pack_forget()
            self.selected_players = []
        
        
    #Method to return to the captain main screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)
        
        
    #Method to expand fixture card to view more details
    def expand_card(self, player):
        self.app.show_expanded_player_card(self.user_id, player)
