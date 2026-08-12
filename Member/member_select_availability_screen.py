import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from SQL import insert_availability_details
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class Member_Select_Availability_Screen(tk.Frame):
    def __init__(self, parent, app, user_id, fixture, fixtures):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.fixture = fixture
        self.fixtures = fixtures
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create the title for the page using a label
        self.title_string = f"{self.fixture['opposition']} ({self.fixture['home_away']}) - {self.fixture['date']}"
        self.lbl_Title = tk.Label(self, text=self.title_string, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="center")
        self.lbl_Title.pack(anchor="center", padx=(10,0), pady=10)
        
        #Create a tick box
        self.is_available = IntVar(value=1)
        self.bx_is_available = Checkbutton(self, text="Are you available?", variable=self.is_available, onvalue=1, offvalue=0, height=3, width=0, bg=c.LIGHT_BACKGROUND, font=c.FONT_LABEL, activebackground=c.LIGHT_BACKGROUND, command=self.toggle_reason_field)
        self.bx_is_available.pack()
        
        #Create a reason why entry and label but do not pack them
        self.lbl_reason = tk.Label(self, text="Reason for unavailability:", font=c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
        self.ent_reason = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
            
        #Create button to confirm
        self.btn_confirm = Rounded_Button(self, text="Confirm", command=self.confirm_availability, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_confirm.pack(pady=15, side="bottom")
        
    
    #Method to toggle the viewing of the entry field 
    def toggle_reason_field(self):
        if self.is_available.get() == 0:
            self.lbl_reason.pack(pady=10)
            self.ent_reason.pack(pady=(0,5))
        else:
            self.lbl_reason.pack_forget()
            self.ent_reason.pack_forget()
        
    
    #Method to check all inputs are valid and confirm the users availability
    def confirm_availability(self):
        if self.is_available.get() == 1:
            insert_availability_details(self.fixture["fixture_id"], self.user_id, self.is_available.get())
            self.app.show_member_availability_screen(self.user_id, self.fixtures)
        else:
            self.reason = self.ent_reason.get().strip()
            if self.reason:
                insert_availability_details(self.fixture["fixture_id"], self.user_id, self.is_available.get(), self.reason)
                self.app.show_member_availability_screen(self.user_id, self.fixtures)
            else:
                messagebox.showinfo(message="A reason for being unavailable is required, please enter one", title="Confirming Availavility Error")
