import tkinter as tk
import constants as c

class Scrollable_Frame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND)
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=c.LIGHT_BACKGROUND, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=c.LIGHT_BACKGROUND)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        
        self.content.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.resize_content)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        
    #Method to update the area that the canvas can scroll through
    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    
    #Method to change the width of the content frame to match the canvas
    def resize_content(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=event.width)
        
        
    #Method to move the canvas up or down when the mouse wheel is used    
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")
        return "break"
    
    
    #Method to bind the mouse wheel scrolling to the frame and all its child widgets
    def bind_children(self):
        #Function that actually binds the mouse wheel event to the widget and all its children
        def bind(widget):
            widget.bind("<MouseWheel>", self.on_mousewheel)
            
            for child in widget.winfo_children():
                bind(child)
                
        bind(self)