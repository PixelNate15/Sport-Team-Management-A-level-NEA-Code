import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.draw_graph import draw_graph
from Reusable_Code.view_player_information import View_Player_Details
from Reusable_Code.Rounded_Items.rounded_button import Rounded_Button
from System.form_score_calculation import calculate_form_score
from SQL import get_last_ten_feedback_scores
import tkinter as tk
from datetime import date
from dateutil.relativedelta import relativedelta


class Captain_Expanded_Player_Card_Screen(tk.Frame):
    def __init__(self, parent, app, user_id, player):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.player = player
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Put title on the screen
        self.title_sentence = f"{player["firstname"]} {player["surname"]}"
        self.title = tk.Label(self, text=self.title_sentence, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put the player details on the screen
        self.player_details = View_Player_Details(self, player)
        self.player_details.pack(side="top", fill="x")
        
        #Put all the graphs on the screen
        self.graph_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(1, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(1, weight=1)

        #Graph 1 - form over last 10 weeks
        self.dates, self.form = self.calculate_form_score_for_10_weeks()
        draw_graph(self.graph_frame, self.dates, self.form, "Form Over 10 Weeks", "Dates", "Form", row=0, column=0)
        
        #Graph 2,3,4 - last 10 (or players total) of all feedback ratings
        self.overall_ratings, self.key_moments_ratings, self.communications_ratings, self.index = self.feedback_score_lists()
        draw_graph(self.graph_frame, self.index, self.overall_ratings, "Overall Ratings", "Index", "Overall Rating", row=0, column=1, want_integer_x_axis=True)
        draw_graph(self.graph_frame, self.index, self.key_moments_ratings, "Key Moments Ratings", "Index", "Key Moments Rating", row=1, column=0, want_integer_x_axis=True)
        draw_graph(self.graph_frame, self.index, self.communications_ratings, "Communications Ratings", "Index", "Communications Rating", row=1, column=1, want_integer_x_axis=True)
        
        #Put back button onto the screen
        self.btn_back = Rounded_Button(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
        
        
    #Method to return to the recent_results_screen
    def return_to_main_screen(self):
        self.app.show_main_screen(self.user_id)
        
        
    #Method to calculate a form score every week for 10 weeks
    def calculate_form_score_for_10_weeks(self):
        dates = []
        form = []
        day_interval = 63
        for i in range(10):
            date_of_form = (date.today() - relativedelta(days=(day_interval - (i * 7))))
            form_from_date = calculate_form_score(self.player["user_id"], date_of_form)
            date_of_form = date_of_form.strftime("%d/%m")
            dates.append(date_of_form)
            form.append(form_from_date)
        return dates, form
    
    
    #Method to get all feedback scores in seperate lists
    def feedback_score_lists(self):
        feedbacks = get_last_ten_feedback_scores(self.player["user_id"])
        
        overall_ratings = []
        key_moments_ratings = []
        communications_ratings = []
        
        for item in feedbacks:
            overall_ratings.append(item["overall_rating"])
            key_moments_ratings.append(item["key_moments_rating"])
            communications_ratings.append(item["communication_rating"])
        
        index = self.list_of_numbers_list_length(overall_ratings)
        return overall_ratings, key_moments_ratings, communications_ratings, index
    
    
    #Method to create a list of numbers based on the length of a list
    def list_of_numbers_list_length(self, lst):
        indexs = []
        for i in range(1, (len(lst) + 1)):
            indexs.append(i)
            
        return indexs
        

            