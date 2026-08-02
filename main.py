import tkinter as tk
import constants as c
from SQL import check_is_captain
from login_screen import Login_Screen
from create_account import Create_Account_Screen
from Member.main_screen_member import Main_Screen_Member
from Member.member_availability_screen import Member_Availability_Screen
from Member.member_select_availability_screen import Member_Select_Availability_Screen
from Member.member_expanded_fixture_card import Member_Expanded_Fixture_Card
from Captain.main_screen_captain import Main_Screen_Captain


class App (tk.Tk):
    def __init__(self):
        super().__init__() #Inhert from the tkinter module
        self.configure(bg=c.LIGHT_BACKGROUND)
        self.iconbitmap("logo_ico.ico")
        self.title("Sports Team Management")
        self.current_frame = None
        self.show_main_screen(2)
        
        
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
            self.current_frame = Main_Screen_Member(self, self, user_id)
            self.current_frame.pack(fill="both", expand="true")
        else:
            self.current_frame = Main_Screen_Captain(self, self, user_id)
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
        
        self.current_frame = Member_Expanded_Fixture_Card(self, self, user_id, fixture)
        self.current_frame.pack(fill="both", expand="true")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
