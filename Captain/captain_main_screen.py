import constants as c
from Reusable_Code.main_screen_sidebar import main_screen_sidebar
from Reusable_Code.player_cards import player_cards
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from SQL.squad import get_players_in_one_squad, remove_player_from_squad
import tkinter as tk
from tkinter import messagebox

class Captain_Main_Screen(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.remove_selection = False
        self.selected_players = []
        
        #Create buttons for sidebar
        self.buttons = [
            ("Manage Fixtures", self.open_manage_fixtures),
            ("All Members", self.open_all_members),
            ("Remove Players", self.toggle_remove_players),
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
        self.app.scrollable_frame.bind_children()
        
          
    #Method to expand fixture card to view more details
    def expand_card(self, player):
        self.app.show_expanded_player_card(self.user_id, player)


    #Method to open the manage fixtures screen
    def open_manage_fixtures(self):
        self.app.show_manage_fixtures_screen(self.user_id)
    

    #Method to open the all members screen
    def open_all_members(self):
        self.app.show_all_players_available_for_squad(self.user_id)
    
    
    #Method to open the my player view screen
    def open_my_player_view(self):
        self.app.current_view = "member"
        self.app.show_main_screen(self.user_id)
        
        
    #Method to toggle between viewing players and selecting players to remove
    def toggle_remove_players(self):
        self.remove_selection = not self.remove_selection
        self.selected_players = []
        
        if self.remove_selection:
            self.sidebar.btn_widgets["Remove Players"].configure_button_text("Cancel Removal")
            
            #Put submit button onto the screen
            self.btn_submit = Rounded_Item(self, text="Submit Removal", command=self.submit_removal, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
            self.btn_submit.pack(pady=15)
        else:
            self.sidebar.btn_widgets["Remove Players"].configure_button_text("Remove Players")
            self.btn_submit.pack_forget()
            
        self._draw_player_cards()
        self.app.scrollable_frame.bind_children()

        
        
    #Method to add/remove the clicked player to the list of players to remove
    def select_player(self, player):
        player_id = player["user_id"]
        
        #The captain cannot remove themselves from their own squad
        if player_id == self.user_id:
            messagebox.showinfo(message="You cannot remove yourself from the squad", title="Remove Players")
            return
        
        if player_id in self.selected_players:
            self.selected_players.remove(player_id)
            self.player_frame.change_colour(player_id, False)
        else:
            self.selected_players.append(player_id)
            self.player_frame.change_colour(player_id, True)
            
            
    #Method to draw the player cards, depending on whether players are being selected
    def _draw_player_cards(self):
        self.player_frame.destroy()
        if self.remove_selection:
            self.player_frame = player_cards(self, self.players, self.select_player, False, self.selected_players, c.LIGHT_ERROR, c.LIGHT_ERROR_HOVER)
        else:
            self.player_frame = player_cards(self, self.players, self.expand_card)
        self.player_frame.pack(after=self.lbl_players)
        self.app.scrollable_frame.bind_children()

        
        
    #Method to move the selected players down to the squad below
    def submit_removal(self):
        if not self.selected_players:
            messagebox.showinfo(message="Cannot move No-one to the squad below", title="Remove Players")
            return
        
        moved = 0
        for player_id in self.selected_players:
            if remove_player_from_squad(player_id):
                moved += 1
        
        if moved == len(self.selected_players):
            messagebox.showinfo(message="Players Moved to the Squad Below", title="Remove Players")
        elif moved == 0:
            messagebox.showinfo(message="There is no squad below yours to move players into", title="Remove Players Error")
        
        #Refreshes the list then leaves removal mode, which also redraws the cards
        self.players = get_players_in_one_squad(self.user_id)
        self.toggle_remove_players()

