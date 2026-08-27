import tkinter as tk
from Member.member_show_selected_fixtures_screen import Member_Show_Selected_Fixtures_Screen
import constants as c
from SQL import check_is_captain
from login_screen import Login_Screen
from create_account import Create_Account_Screen
from Member.member_main_screen import Member_Main_Screen
from Member.member_availability_screen import Member_Availability_Screen
from Member.member_select_availability_screen import Member_Select_Availability_Screen
from Member.member_expanded_fixture_card_screen import Member_Expanded_Fixture_Card_Screen
from Member.member_show_recent_results_screen import Member_Show_Recent_Results
from Member.member_expanded_result_card_screen import Member_Expanded_Result_Card_Screen
from Member.member_show_recent_partner_feedback import Member_Recent_Partner_Feedback
from Member.member_show_required_partner_feedback_screen import Member_Show_Required_Partner_Feedback
from Member.member_submit_feedback import Member_Sumbit_Feedback
from Member.member_view_injury_status_screen import Member_View_Injury_Status
from Member.member_edit_injury_status_screen import Member_Edit_Injury_Status
from Captain.captain_main_screen import Captain_Main_Screen
from Captain.captain_expanded_player_card import Captain_Expanded_Player_Card_Screen


class App (tk.Tk):
    def __init__(self):
        super().__init__() #Inhert from the tkinter module
        self.configure(bg=c.LIGHT_BACKGROUND)
        self.iconbitmap("logo_ico.ico")
        self.title("Sports Team Management")
        self.current_frame = None
        self.show_main_screen(1)
        
        
    #Method to clear the screen of the current frame
    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
            
            
    #Method to show the login screen frame
    def show_login_screen(self):
        self.clear_screen()
        self.geometry("550x400")
        
        self.current_frame = Login_Screen(self, self)
        self.current_frame.pack(fill="both", expand="true")

    
    #Method to show the create account frame
    def show_create_account(self):
        self.clear_screen()
        self.geometry("550x740")

        self.current_frame = Create_Account_Screen(self, self)
        self.current_frame.pack(fill="both", expand="true")


    #Method to show the main screen frame
    def show_main_screen(self, user_id):
        self.clear_screen()
        self.geometry("800x768")

        self.is_captain = check_is_captain(user_id)

        if self.is_captain == False:
            self.current_frame = Member_Main_Screen(self, self, user_id)
            self.current_frame.pack(fill="both", expand="true")
        else:
            self.current_frame = Captain_Main_Screen(self, self, user_id)
            self.current_frame.pack(fill="both", expand="true")
            
    
    #Method to show the availability screen for the member
    def show_member_availability_screen(self, user_id, fixtures):
        self.clear_screen()
        self.geometry("550x675")
        
        self.current_frame = Member_Availability_Screen(self, self, user_id, fixtures)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the select availability screen for the member
    def show_member_select_availability_screen(self, user_id, fixture, fixtures):
        self.clear_screen()
        self.geometry("550x450")
        
        self.current_frame = Member_Select_Availability_Screen(self, self, user_id, fixture, fixtures)
        self.current_frame.pack(fill="both", expand="true")
        
        
        
    #Method to show the view fixture information screen
    def show_expanded_fixture(self, user_id, fixture):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Expanded_Fixture_Card_Screen(self, self, user_id, fixture)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the view selected fixtures screen
    def show_selected_fixtures(self, user_id, fixtures):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Show_Selected_Fixtures_Screen(self, self, user_id, fixtures)
        self.current_frame.pack(fill="both", expand="true")
        
    
    #Method to show the recent results for a member
    def show_recent_results(self, user_id):
        self.clear_screen()
        self.geometry("550x715")
        
        self.current_frame = Member_Show_Recent_Results(self, self, user_id)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the view result information screen
    def show_expanded_result(self, user_id, result):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Expanded_Result_Card_Screen(self, self, user_id, result)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the recent partner feedback screen
    def show_recent_partner_feedback(self, user_id):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Recent_Partner_Feedback(self, self, user_id)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the required partner feedback screen
    def show_required_partner_feedback(self, user_id):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Show_Required_Partner_Feedback(self, self, user_id)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the submit partner feedback screen
    def show_submit_partner_feedback(self, user_id, result):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Sumbit_Feedback(self, self, user_id, result)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show the view injury status screen
    def show_view_injury_status(self, user_id):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_View_Injury_Status(self, self, user_id)
        self.current_frame.pack(fill="both", expand="true")
        
        
    #Method to show submit injury status screen
    def show_submit_injury_status(self, user_id, injury):
        self.clear_screen()
        self.geometry("550x650")
        
        self.current_frame = Member_Edit_Injury_Status(self, self, user_id, injury)
        self.current_frame.pack(fill="both", expand="true")
        
    
    #Method to show the expanded player card screen
    def show_expanded_player_card(self, user_id, player):
        self.clear_screen()
        self.geometry("900x1150")
        
        self.current_frame = Captain_Expanded_Player_Card_Screen(self, self, user_id, player)
        self.current_frame.pack(fill="both", expand="true")


if __name__ == "__main__":
    app = App()
    app.mainloop()
