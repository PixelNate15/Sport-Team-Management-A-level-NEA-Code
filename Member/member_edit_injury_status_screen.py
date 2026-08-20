import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from SQL import remove_injury_status, member_update_injury_status, insert_injury_status
import tkinter as tk
from tkinter import *
from tkcalendar import DateEntry
from datetime import date
from tkinter import messagebox

class Member_Edit_Injury_Status(tk.Frame):
    def __init__(self, parent, app, user_id, injury):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.injury = injury
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Create title label
        self.lbl_title = tk.Label(self, text="Edit Injury Status", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put the data inputs onto the screen
        self.lbl_injury = tk.Label(self, text="Injury:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_injury.pack()
        self.ent_injury = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=50)
        self.ent_injury.pack(pady=(0,5))
        self.ent_injury.insert(0, (self.injury["description"] if self.injury else ""))
        
        self.lbl_expected_return_date = tk.Label(self, text="Expected Return Date:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_expected_return_date.pack()
        self.ent_expected_return_date = DateEntry(self, width=15, date_pattern="dd/mm/yyyy")
        self.ent_expected_return_date.pack(pady=(0,10))
        self.ent_expected_return_date.set_date((self.injury["expected_end_date"] if self.injury else date.today()))
        
        self.lbl_can_you_play = tk.Label(self, text="Can You Play:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_can_you_play.pack()
        self.can_play = IntVar(value=self.injury["can_play"] if self.injury else 1)
        self.bx_can_play = Checkbutton(self, variable=self.can_play, onvalue=1, offvalue=0, height=0, width=0, bg=c.LIGHT_BACKGROUND, font=c.FONT_LABEL, activebackground=c.LIGHT_BACKGROUND)
        self.bx_can_play.pack()
        
        self.lbl_notes = tk.Label(self, text="Notes:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_notes.pack()
        self.txt_notes = tk.Text(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, width=50, height=6)
        self.txt_notes.pack()
        self.txt_notes.insert("1.0", self.injury["notes"] if self.injury else "")
        
        #Put no injury, submit and back buttons on the screen
        self.btn_no_injury = Rounded_Button(self, text="No Injury", command=self.clear_injury_status, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_no_injury.pack(pady=15)
        self.btn_submit = Rounded_Button(self, text="Submit", command=self.submit_injury_status, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_submit.pack(pady=15)
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_view_injury_status, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
    
    #Method to clear the user of any injury
    def clear_injury_status(self):
        if not self.injury:
            messagebox.showinfo(message="Already no injury", title="No Injury")
            return
        remove_injury_status(self.injury["injury_id"])
        self.return_to_view_injury_status()
       
        
    #Method to submit the updated injury status
    def submit_injury_status(self):
        self.description = self.ent_injury.get().strip()
        self.expected_return_date = self.ent_expected_return_date.get_date()
        self.notes = self.txt_notes.get("1.0", tk.END).strip()
        if self.description and self.expected_return_date >= date.today() and self.notes:
            if self.injury:
                member_update_injury_status(self.injury["injury_id"], self.description, self.expected_return_date, self.can_play.get(), self.notes)
                messagebox.showinfo(message="Injury Status Updated", title="Injury Status")
                self.return_to_view_injury_status()
                return
            insert_injury_status(self.user_id, self.description, self.expected_return_date, self.can_play.get(), self.notes)
            messagebox.showinfo(message="Injury Status Added", title="Injury Status")
            self.return_to_view_injury_status()
            return
        else:
            messagebox.showinfo(message="Please fully fill in the fields", title="Missing Data")
        
    #Method to return to login screen
    def return_to_view_injury_status(self):
        self.app.show_view_injury_status(self.user_id)