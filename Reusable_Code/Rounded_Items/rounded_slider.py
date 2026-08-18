from Reusable_Code.Rounded_Items.rounded_shapes import draw_rounded_rect
import constants as c
import tkinter as tk

class Rounded_Slider(tk.Canvas):
    def __init__(self, parent, parent_bg, min_value=0, max_value=10, width=300, height=30, track_colour=c.LIGHT_SIDEBAR, fill_colour=c.LIGHT_PRIMARY_ACCENT, handle_colour=c.LIGHT_PRIMARY_ACCENT, command=None):
        super().__init__(parent, width=width, height=height, bg=parent_bg, highlightthickness=0)
        self.min_value = min_value
        self.max_value = max_value
        self.width = width
        self.height = height
        self.track_colour = track_colour
        self.fill_colour = fill_colour
        self.handle_colour = handle_colour
        self.command = command
        self.value = min_value
        self.track_y = height / 2
        self.handle_radius = 10

        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_click)

        self._draw()
        
    
    #Method to draw the slider
    def _draw(self):
        self.delete("all")
        draw_rounded_rect(self, 5, self.track_y - 4, self.width - 5, self.track_y + 4, radius=4, fill_colour=self.track_colour)
        
        handle_x = self._value_to_x(self.value)
        draw_rounded_rect(self, 5, self.track_y - 4, handle_x, self.track_y + 4, radius=4, fill_colour=self.fill_colour)

        self.create_oval(handle_x - self.handle_radius, self.track_y - self.handle_radius,
                          handle_x + self.handle_radius, self.track_y + self.handle_radius,
                          fill=self.handle_colour, outline="")


    #Method to turn the value of the slider to the x-coordinate
    def _value_to_x(self, value):
        usable_width = self.width - 10
        ratio = (value - self.min_value) / (self.max_value - self.min_value)
        return (5 + (ratio * usable_width))


    #Method to turn the x coordinate to the value of the slider
    def _x_to_value(self, x):
        usable_width = self.width - 10
        ratio = max(0, min(1, (x - 5) / usable_width))
        raw_value = self.min_value + (ratio * (self.max_value - self.min_value))
        return (round(raw_value))


    #Method to get the value of the slider and redraw it when clicked
    def _on_click(self, event):
        self.value = self._x_to_value(event.x)
        self._draw()
        if self.command:
            self.command(self.value)


    #Method to return the value of the slider
    def get(self):
        return self.value