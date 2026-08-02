import constants as c
from Reusable_Code.reusable_buttons import add_hover
from SQL import insert_account_details, check_for_duplicate_username
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date
import bcrypt as b


class Create_Account_Screen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app

        #Create the main title
        self.lbl_main_title = tk.Label(self, text="Sport's Team Management", font=c.FONT_TITLE, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_main_title.pack(pady=(0,10))

        #Create firstname and surname label and entry
        self.lbl_firstname = tk.Label(self, text="Firstname:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_firstname.pack(pady=10)
        self.ent_firstname = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_firstname.pack(pady=(0,5))
        
        self.lbl_surname = tk.Label(self, text="Surname:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_surname.pack(pady=10)
        self.ent_surname = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_surname.pack(pady=(0,5))

        #Create the date of birth input
        self.lbl_dob = tk.Label(self, text="Date Of Birth:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_dob.pack()
        self.ent_dob = DateEntry(self, width=15, date_pattern="dd/mm/yyyy")
        self.ent_dob.pack(pady=(0,10))

        #Create the generate username button
        self.btn_generate_username = tk.Button(self, text="Generate Username", font=c.FONT_BUTTON, bg=c.LIGHT_PRIMARY_ACCENT, fg="white", activebackground=c.DARK_PRIMARY_ACCENT, activeforeground="white", command=self.generate_username)
        add_hover(self.btn_generate_username, c.LIGHT_PRIMARY_ACCENT, c.LIGHT_ACCENT_HOVER)
        self.btn_generate_username.pack(pady=(0,10))

        #Creates the username label and entry and inserts the generated username into it
        self.lbl_username = tk.Label(self, text="Username:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_username.pack(pady=(0,10))
        self.ent_username = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", state="readonly")
        self.ent_username.pack(pady=(0,5))

        #Create the email and password label and entry
        self.lbl_email = tk.Label(self, text="Email:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_email.pack(pady=10)
        self.ent_email = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_email.pack(pady=(0,5))
        
        self.lbl_password1 = tk.Label(self, text="Password:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_password1.pack(pady=10)
        self.ent_password1 = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", show="*")
        self.ent_password1.pack(pady=(0,15))

        self.lbl_password2 = tk.Label(self, text="Re-enter Password:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_password2.pack(pady=10)
        self.ent_password2 = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", show="*")
        self.ent_password2.pack(pady=(0,15))

        #Create the create account button
        self.btn_create_account = tk.Button(self, text="Create Account", font=c.FONT_BUTTON, bg=c.LIGHT_PRIMARY_ACCENT, fg="white", activebackground=c.DARK_PRIMARY_ACCENT, activeforeground="white", command=self.create_account, state="disabled")
        add_hover(self.btn_create_account, c.LIGHT_PRIMARY_ACCENT, c.LIGHT_ACCENT_HOVER)
        self.btn_create_account.pack(pady=(0,10))


    #Method to generate a users username from their firstname and surname and date of birth
    def generate_username(self):
        self.firstname = self.ent_firstname.get().strip()
        self.surname = self.ent_surname.get().strip()
        self.dob = self.ent_dob.get_date()
        if (self.firstname) and (self.surname) and (self.dob < date.today()):
            self.isUsernameGenerated = False
            self.count = 0
            self.username = (self.firstname[:3]) + (self.surname[:3]) + (str(self.dob.year)[-2:])
            self.base = self.username
            while (self.isUsernameGenerated == False):
                if (check_for_duplicate_username(self.username) == False):
                    self.ent_username.config(state="normal")
                    self.ent_username.delete(0, tk.END)
                    self.ent_username.insert(0, self.username)
                    self.ent_username.config(state="readonly")
                    self.isUsernameGenerated = True
                    self.btn_create_account.config(state="normal")
                else:
                    self.count += 1
                    self.username = self.base + str(self.count)  
        else:
            messagebox.showinfo(message="Username cannot be generated without sufficient information, try again", title="Username Generation Error")

    
    #Method to create an account
    def create_account(self):
        self.email = self.ent_email.get().strip()
        self.password1 = self.ent_password1.get().strip()
        self.password2 = self.ent_password2.get().strip()
        if (self.email) and (self.password1) and (self.password1 == self.password2):
            self.hashed_password = b.hashpw(self.password1.encode('utf-8'), b.gensalt())
            self.user_id = insert_account_details(self.firstname, self.surname, self.dob, self.username, self.hashed_password, self.email)
            self.app.show_main_screen(self.user_id)