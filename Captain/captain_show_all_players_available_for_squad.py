import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.player_cards import player_cards
from SQL import get_club_id, get_all_players_for_squads_below_ranking
import tkinter as tk


class Captain_Show_All_Players_Available_For_Squad(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
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
        self.filter_grid.pack(pady=10)
        
        self.ent_search = tk.Entry(self.filter_grid, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_search.grid(row=0, column=0)
        self.btn_search = Rounded_Button(self.filter_grid, text="Search", command=self.filter_player_cards, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_search.grid(row=0, column=1)
        
        #Create player cards for all players in the captains squad ranking and below rankings
        self.club_id = get_club_id(self.user_id)
        self.players = get_all_players_for_squads_below_ranking(self.user_id, self.club_id)
        self.player_frame = player_cards(self, self.players, self.expand_card, True)
        self.player_frame.pack(fill="both", expand=True)
                
                
        #Put back button onto the screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to filter player cards
    def filter_player_cards(self):
        self.search = self.ent_search.get().strip().split()
        if len(self.search) == 1:
            for player in self.players:
                if player["firstname"].lower() == self.search[0].lower() or player["surname"].lower() == self.search[0].lower():
                    self.player_frame.destroy()
                    self.player_list = [player]
                    self.player_frame = player_cards(self, self.player_list, self.expand_card)
                    self.player_frame.pack(fill="both", expand=True)
        elif len(self.search) == 2:
            for player in self.players:
                if player["firstname"].lower() == self.search[0].lower() and player["surname"].lower() == self.search[1].lower():
                    self.player_frame.destroy()
                    self.player_list = [player]
                    self.player_frame = player_cards(self, self.player_list, self.expand_card)
                    self.player_frame.pack(fill="both", expand=True)
        elif len(self.search) == 0:
            self.player_frame.destroy()
            self.player_frame = player_cards(self, self.players, self.expand_card, True)
            self.player_frame.pack(fill="both", expand=True)
        else:
            self.player_frame.destroy()       
        
        
    #Method to return to the recent_results_screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)
        
        
    #Method to expand fixture card to view more details
    def expand_card(self, player):
        self.app.show_expanded_player_card(self.user_id, player)