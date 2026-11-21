import tkinter as tk
import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.scrollable_frame import Scrollable_Frame
from SQL import check_is_captain
from login_screen import Login_Screen
from create_account import Create_Account_Screen
from Member.member_main_screen import Member_Main_Screen
from Member.member_availability_screen import Member_Availability_Screen
from Member.member_select_availability_screen import Member_Select_Availability_Screen
from Member.member_expanded_fixture_card_screen import Member_Expanded_Fixture_Card_Screen
from Member.member_show_selected_fixtures_screen import Member_Show_Selected_Fixtures_Screen
from Member.member_show_recent_results_screen import Member_Show_Recent_Results
from Member.member_expanded_result_card_screen import Member_Expanded_Result_Card_Screen
from Member.member_show_recent_partner_feedback import Member_Recent_Partner_Feedback
from Member.member_show_required_partner_feedback_screen import Member_Show_Required_Partner_Feedback
from Member.member_submit_feedback import Member_Sumbit_Feedback
from Member.member_view_injury_status_screen import Member_View_Injury_Status
from Member.member_edit_injury_status_screen import Member_Edit_Injury_Status
from Captain.captain_main_screen import Captain_Main_Screen
from Captain.captain_expanded_player_card import Captain_Expanded_Player_Card_Screen
from Captain.captain_show_all_players_available_for_squad import Captain_Show_All_Players_Available_For_Squad
from Captain.captain_manage_fixtures import Captain_Manage_Fixtures
from Captain.captain_add_or_edit_fixture import Captain_Add_Or_Edit_Fixture
from Captain.captain_show_fixtures_needing_results import Captain_Show_Fixtures_Needing_Results
from Captain.captain_add_or_edit_result import Captain_Add_Or_Edit_Result


class App (tk.Tk):
    def __init__(self):
        super().__init__() #Inhert from the tkinter module
        self.configure(bg=c.LIGHT_BACKGROUND)
        self.iconbitmap("logo_ico.ico")
        self.title("Sports Team Management")
        self.current_frame = None
        self.current_screen = None
        self.scrollable_frame = None
        self.header = None
        self.current_view = None
        self.show_main_screen(1)
        
        
    #Method to clear the screen of the current frame
    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
            self.current_screen = None
            self.scrollable_frame = None
            self.header = None


    #Method to put any program screen inside a full-window scrollable frame
    def show_screen(self, screen_class, geometry, *screen_args, show_header=True):
        #Clear the current screen
        self.clear_screen()

        #Get the width and height from the geometry
        width, height = (int(value) for value in geometry.split("x", 1))

        #Make sure the window height fits on the users screen
        available_height = max(200, self.winfo_screenheight() - 100)
        window_height = min(height, available_height)
        self.geometry(f"{width}x{window_height}")

        #Create the frame which holds the header and scrollable frame
        self.current_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.current_frame.pack(fill="both", expand=True)

        #Put a fixed header onto the screen if one is required
        if show_header:
            self.header = Header_Panel(self.current_frame)
            self.header.pack(side="top", fill="x")

        #Create the scrollable frame underneath the header
        self.scrollable_frame = Scrollable_Frame(self.current_frame, width=width, height=height)
        self.scrollable_frame.pack(fill="both", expand=True)

        #Create the required screen inside the scrollable frame
        self.current_screen = screen_class(self.scrollable_frame.content, self, *screen_args)
        self.current_screen.pack(fill="both", expand=True)
            
            
    #Method to show the login screen frame
    def show_login_screen(self):
        self.show_screen(Login_Screen, "550x400", show_header=False)

        
    #Method to show the create account frame
    def show_create_account(self):
        self.show_screen(Create_Account_Screen, "550x740", show_header=False)


    #Method to show the main screen frame
    def show_main_screen(self, user_id):
        self.is_captain = check_is_captain(user_id)

        if self.is_captain == False or self.current_view == "member":
            self.current_view = "member"
            self.show_screen(Member_Main_Screen, "800x768", user_id)
        else:
            self.current_view = "captain"
            self.show_screen(Captain_Main_Screen, "800x768", user_id)
            
    
    #Method to show the availability screen for the member
    def show_member_availability_screen(self, user_id):
        self.show_screen(Member_Availability_Screen, "550x775", user_id)
        
        
    #Method to show the select availability screen for the member
    def show_member_select_availability_screen(self, user_id, fixture, filter):
        self.show_screen(Member_Select_Availability_Screen, "550x450", user_id, fixture, filter)
        
         
    #Method to show the view fixture information screen
    def show_expanded_fixture(self, user_id, fixture):
        self.show_screen(Member_Expanded_Fixture_Card_Screen, "550x650", user_id, fixture)
        
        
    #Method to show the view selected fixtures screen
    def show_selected_fixtures(self, user_id, fixtures):
        self.show_screen(Member_Show_Selected_Fixtures_Screen, "550x650", user_id, fixtures)
        
    
    #Method to show the recent results for a member
    def show_recent_results(self, user_id):
        self.show_screen(Member_Show_Recent_Results, "550x715", user_id)
        
        
    #Method to show the view result information screen
    def show_expanded_result(self, user_id, result):
        self.show_screen(Member_Expanded_Result_Card_Screen, "550x650", user_id, result)
        
        
    #Method to show the recent partner feedback screen
    def show_recent_partner_feedback(self, user_id):
        self.show_screen(Member_Recent_Partner_Feedback, "550x650", user_id)
        
        
    #Method to show the required partner feedback screen
    def show_required_partner_feedback(self, user_id):
        self.show_screen(Member_Show_Required_Partner_Feedback, "550x650", user_id)
        
        
    #Method to show the submit partner feedback screen
    def show_submit_partner_feedback(self, user_id, result):
        self.show_screen(Member_Sumbit_Feedback, "550x820", user_id, result)
        
        
    #Method to show the view injury status screen
    def show_view_injury_status(self, user_id):
        self.show_screen(Member_View_Injury_Status, "550x650", user_id)
        
        
    #Method to show submit injury status screen
    def show_submit_injury_status(self, user_id, injury):
        self.show_screen(Member_Edit_Injury_Status, "550x720", user_id, injury)
        
    
    #Method to show the expanded player card screen
    def show_expanded_player_card(self, user_id, player):
        self.show_screen(Captain_Expanded_Player_Card_Screen, "900x1150", user_id, player)
        
        
    #Method to show the all available players for squad screen
    def show_all_players_available_for_squad(self, user_id):
        self.show_screen(Captain_Show_All_Players_Available_For_Squad, "1100x1150", user_id)
        
        
    #Method to show the manage fixtures screen
    def show_manage_fixtures_screen(self, user_id):
        self.show_screen(Captain_Manage_Fixtures, "1200x800", user_id)
        
        
    #Method to show the add/edit fixture screen
    def show_add_or_edit_fixture_screen(self, user_id, is_new, fixture_id=None):
        self.show_screen(Captain_Add_Or_Edit_Fixture, "1200x1300", user_id, is_new, fixture_id)
        
        
    #Method to show the fixtures that need results screen
    def show_fixtures_needing_results(self, user_id):
        self.show_screen(Captain_Show_Fixtures_Needing_Results, "550x650", user_id)
        
        
    #Method to show the add/edit fixture screen
    def show_add_or_edit_result_screen(self, user_id, is_new, fixture_id):
        self.show_screen(Captain_Add_Or_Edit_Result, "1200x1300", user_id, is_new, fixture_id)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
