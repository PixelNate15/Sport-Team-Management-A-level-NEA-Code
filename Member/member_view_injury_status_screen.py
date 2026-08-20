import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.view_injury_information import View_Injury_Details
from SQL import get_injury_info
import tkinter as tk

class Member_View_Injury_Status(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create title label
        self.lbl_title = tk.Label(self, text="Injury Status", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Puts injury information onto the screen
        self.injury = get_injury_info(self.user_id)
        self.injury_details = View_Injury_Details(self, self.injury)
        self.injury_details.pack(side="top", fill="x")
        
        #Create both the edit and back buttons
        self.btn_edit = Rounded_Button(self, text="Edit", command=self.edit_injury_status, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_edit.pack(pady=15)
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to return to login screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)
        
        
    #Method to transfer to edit injury status screen
    def edit_injury_status(self):
        self.app.show_submit_injury_status(self.user_id, self.injury)