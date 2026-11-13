import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.view_result_information_captain import View_Result_Details
from Reusable_Code.results_table import Result_Table
from SQL import get_result
import tkinter as tk
from tkinter import messagebox


class Captain_Add_Or_Edit_Result(tk.Frame):
    def __init__(self, parent, app, user_id, is_new, fixture_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        self.is_new = is_new
        self.fixture_id = fixture_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Puts the title on the screen
        self.title_text = "Add Result" if is_new else "Edit Result"
        self.title = tk.Label(self, text=self.title_text, font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.title.pack(anchor="w", padx=(10,0), pady=10)
        
        #Put the result details on the screen
        self.result_details_info = get_result(self.fixture_id)
        self.result_details = View_Result_Details(self, self.result_details_info)
        self.result_details.pack(side="top", fill="x")
        
        self.score_grid = Result_Table(self, players=["James / Oliver", "Harry / George", "James / Harry", "Oliver / George"])
        self.score_grid.pack(pady=10)