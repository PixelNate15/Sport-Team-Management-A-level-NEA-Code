import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from Reusable_Code.Rounded_Items.rounded_slider import Rounded_Slider
from SQL import get_partner_info, insert_partner_feedback
import tkinter as tk
from tkinter import messagebox

class Member_Sumbit_Feedback(tk.Frame):
    def __init__(self, parent, app, user_id, result):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.result = result
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Label to put the title label on the screen
        self.partner = get_partner_info(self.user_id, self.result["match_id"])
        self.partner_name = self.partner["firstname"] + " " + self.partner["surname"]
        title_sentence = f"Feedback: {self.partner_name} - {self.result["opposition"]} ({self.result["date"]})"
        self.lbl_partnerfeedback = tk.Label(self, text=title_sentence, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_partnerfeedback.pack(pady=(10,0))
        
        #Puts the rating section on the screen
        self.lbl_communication = tk.Label(self, text="Communication Rating:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_communication.pack(pady=10)
        self.slider_communication = Rounded_Slider(self, c.LIGHT_BACKGROUND, command=self.update_communication_value)
        self.slider_communication.pack()
        self.lbl_communication_value = tk.Label(self, text=self.slider_communication.get(), font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_communication_value.pack(pady=10)
        
        self.lbl_key_moments = tk.Label(self, text="Key Moments Rating:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_key_moments.pack(pady=10)
        self.slider_key_moments = Rounded_Slider(self, c.LIGHT_BACKGROUND, command=self.update_key_moments_value)
        self.slider_key_moments.pack()
        self.lbl_key_moments_value = tk.Label(self, text=self.slider_key_moments.get(), font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_key_moments_value.pack(pady=10)
        
        self.lbl_overall = tk.Label(self, text="Overall Rating:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_overall.pack(pady=10)
        self.slider_overall = Rounded_Slider(self, c.LIGHT_BACKGROUND, command=self.update_overall_value)
        self.slider_overall.pack()
        self.lbl_overall_value = tk.Label(self, text=self.slider_overall.get(), font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_overall_value.pack(pady=10)
        
        self.lbl_comment = tk.Label(self, text="Comment:", font=c.FONT_HEADING, fg=c.LIGHT_SECONDARY_TEXT, bg=c.LIGHT_BACKGROUND)
        self.lbl_comment.pack(pady=10)
        self.ent_comment = tk.Entry(self, font =c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=50)
        self.ent_comment.pack(pady=(0,5))
        
        #Create back and submit buttons
        self.btn_submit = Rounded_Button(self, text="Submit Feedback", command=self.submit_feedback, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_submit.pack(pady=15)
        
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_required_feedback_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
            
    
    #Method to update the communication value 
    def update_communication_value(self, value):
        self.lbl_communication_value.config(text=value)
        
    
    #Method to update the key_moments value 
    def update_key_moments_value(self, value):
        self.lbl_key_moments_value.config(text=value)
        
        
    #Method to update the overall value 
    def update_overall_value(self, value):
        self.lbl_overall_value.config(text=value)
        
    
    #Method to return to the previous screen
    def return_to_required_feedback_screen(self):
        self.app.show_required_partner_feedback(self.user_id)
        
    
    #Method to submit the feedback with the entry validated then return to the previous page  
    def submit_feedback(self):
        self.communication_score = self.slider_communication.get()
        self.key_moments_score = self.slider_key_moments.get()
        self.overall_score = self.slider_overall.get()
        self.comment = self.ent_comment.get().strip()
        if self.comment:
            insert_partner_feedback(self.result["match_id"], self.user_id, self.partner["user_id"], self.overall_score, self.key_moments_score, self.communication_score, self.comment)
            self.app.show_required_partner_feedback(self.user_id)
        else:
            messagebox.showinfo(message="Please write a comment", title="Submit Feedback Error")
