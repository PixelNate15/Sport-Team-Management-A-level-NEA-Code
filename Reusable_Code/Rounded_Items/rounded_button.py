import tkinter as tk
from Reusable_Code.Rounded_Items.rounded_shapes import draw_rounded_rect

#Creates a rounded button
class Rounded_Button(tk.Canvas):
    def __init__(self, parent, text, command, font, bg_colour, hover_colour, fg_colour, parent_bg, width=170, height=42, radius=16):
        super().__init__(parent, width=width, height=height, bg=parent_bg, highlightthickness=0)
        
        self.command = command
        self.bg_colour = bg_colour
        self.hover_colour = hover_colour
        
        self._draw(bg_colour, text, font, fg_colour, width, height, radius)
        
        #Bind click and hover the same way you'd bind them to a real Button
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self._draw(self.hover_colour, text, font, fg_colour, width, height, radius))
        self.bind("<Leave>", lambda e: self._draw(self.bg_colour, text, font, fg_colour, width, height, radius))
        
        
    #Method to draw the rounded buttons
    def _draw(self, colour, text, font, fg_colour, width, height, radius):
        self.delete("all")
        draw_rounded_rect(self, 0, 0, width, height, radius, colour)
        self.create_text((width / 2), (height / 2), text=text, font=font, fill=fg_colour, width=(width - 20))