import tkinter as tk
from Reusable_Code.Rounded_Items.rounded_shapes import draw_rounded_rect

#Creates a rounded card in a canvas
class Rounded_Card(tk.Frame):
    def __init__(self, parent, width, height, radius, bg_colour, parent_bg_colour, hover_colour):
        super().__init__(parent, bg=parent_bg_colour)
        
        self.width = width
        self.height = height
        self.radius = radius
        self.bg_colour = bg_colour
        self.hover_colour = hover_colour
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent_bg_colour, highlightthickness=0)
        self.canvas.pack()
        
        self._draw(self.bg_colour)
        
        #Creates content frame which sits on top of drawn shape
        self.content = tk.Frame(self.canvas, bg=self.bg_colour)
        self.canvas.create_window((width / 2), (height / 2), window=self.content)
        
        
    #Method to redraw the card for the given colour
    def _draw(self, colour):
        self.canvas.delete("card_background")
        draw_rounded_rect(self.canvas, 0, 0, self.width, self.height, self.radius, colour, tag="card_background")
        self.canvas.tag_lower("card_background")
        
        
    #Method to change the set colour to draw the card in
    def set_colour(self, colour):
        self._draw(colour)
        self.content.config(bg=colour)
        for child in self.content.winfo_children():
            child.config(bg=colour)        
