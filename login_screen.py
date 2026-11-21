import constants as c
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
import tkinter as tk
from tkinter import messagebox
from SQL import check_password_hash, get_user_id
import bcrypt as b


class Login_Screen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app

        #Create the main title
        self.lbl_main_title = tk.Label(self, text="Sport's Team Management", font=c.FONT_TITLE, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_main_title.pack(pady=(0,25))

        #Create username and password label and entry
        self.lbl_username = tk.Label(self, text="Username:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_username.pack(pady=10)
        self.ent_username = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center")
        self.ent_username.pack(pady=(0,5))

        self.lbl_password = tk.Label(self, text="Password:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_password.pack(pady=10)
        self.ent_password = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", show="*")
        self.ent_password.pack(pady=(0,15))

        #Creates the login button and create new account buttons
        self.btn_login = Rounded_Item(self, text="Login", command=self.login, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_login.pack(pady=(0,20))

        self.btn_create_account = Rounded_Item(self, text="Create Account", command=self.create_account, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_create_account.pack()
        self.app.scrollable_frame.bind_children()


    #Method to check login details are correct and if so log the user in
    def login(self):
        self.username = self.ent_username.get().strip()
        self.password = self.ent_password.get().strip()
        if (self.username) and (self.password):
            self.stored_hash = check_password_hash(self.username)
            if self.stored_hash and b.checkpw(self.password.encode('utf-8'), self.stored_hash.encode('utf-8')):
                self.user_id = get_user_id(self.username)
                self.app.show_main_screen(self.user_id)
            else:
                messagebox.showinfo(message="Login failed, try again", title="Login Error")
        else:
            messagebox.showinfo(message="Login failed, try again", title="Login Error")


    #Method to transfer to user to create account frame if they click that button
    def create_account(self):
        self.app.show_create_account()
