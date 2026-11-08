import constants as c
from Reusable_Code.main_screen_header_panel import Header_Panel
from Reusable_Code.Rounded_Items.rounded_item import Rounded_Item
from Reusable_Code.scrollable_frame import Scrollable_Frame
from SQL import get_fixtures
import tkinter as tk

class Captain_Main_Screen(tk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        self.app = app
        self.user_id = user_id
        
        #Puts header on the screen
        self.header = Header_Panel(self)
        self.header.pack(side="top", fill="x")
        
        #Creates the main frame to hold both columns in
        self.main_frame = tk.Frame(self, bg=c.LIGHT_BACKGROUND)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=10)        
        
        #Configure the frame into three columns
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="fixture_columns")
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1, uniform="fixture_columns")
        
        #Configure the frame so the row with scrollable frames can expand
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        #Create the title labels
        self.lbl_upcoming = tk.Label(self, text="Upcoming Fixtures", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_upcoming.pack(anchor="w", padx=(10,0), pady=10)
        
        self.lbl_results = tk.Label(self, text="Results", font=c.FONT_HEADING, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="right")
        self.lbl_results.pack(anchor="w", padx=(10,0), pady=10)
        
        #Creates the divider across the middle
        self.middle_divider = tk.Frame(self.main_frame, bg=c.LIGHT_MAIN_TEXT, width=2)
        self.middle_divider.grip(row=0, column=2, rowspan=2, sticky="ns", padx=10)
        
        #Creates the scrollable frames
        self.upcoming_scroll = Scrollable_Frame(self.main_frame, width=540, height=400)
        self.upcoming_scroll.grid(row=1, column=0, sticky="nsew", padx=5)

        self.results_scroll = Scrollable_Frame(self.main_frame, width=540, height=400)
        self.results_scroll.grid(row=1, column=2, sticky="nsew", padx=5)
        #Finish
        
        #Put back button onto the screen
        self.btn_back = Rounded_Item(self, text="Back", command=self.return_to_main_screen, font=c.FONT_BUTTON, bg_colour=c.LIGHT_PRIMARY_ACCENT, hover_colour=c.LIGHT_ACCENT_HOVER, fg_colour="white", width=170, height=42, radius=16, parent_bg_colour=c.LIGHT_BACKGROUND)
        self.btn_back.pack(pady=15)
      
      
        #Method to return to the recent_results_screen
        def return_to_main_screen(self):
            self.app.show_main_screen(self.user_id)
            