import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.main_screen_sidebar import main_screen_sidebar
from Reusable_Code.player_cards import player_cards
from SQL import get_players_in_one_squad
import tkinter as tk

class Captain_Main_Screen(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create buttons for sidebar
        self.buttons = [
            ("Manage Fixtures", self.open_manage_fixtures),
            ("Team Graphs", self.open_team_graphs),
            ("All Members", self.open_all_members),
            ("My Player View", self.open_my_player_view)
        ]
        #Put sidebar on screen
        self.sidebar = main_screen_sidebar(self, self.buttons)
        self.sidebar.pack(side="left", fill="y")
        
        #Create label for players
        self.lbl_players = tk.Label(self, text="Players", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_players.pack(anchor="w", padx=(10,0), pady=10)
        
        #Get list of players
        self.players = get_players_in_one_squad(self.user_id)
        self.player_frame = player_cards(self, self.players, self.expand_card)
        self.player_frame.pack()
        
          
    #Method to expand fixture card to view more details
    def expand_card(self, fixture):
        pass


    #Method to open the manage fixtures screen
    def open_manage_fixtures(self):
        pass
    
    
    #Method to open the team graphs screen
    def open_team_graphs(self):
        pass
    
    
    #Method to open the all members screen
    def open_all_members(self):
        pass
    
    
    #Method to open the my player view screen
    def open_my_player_view(self):
        pass