import tkinter as tk
from Reusable_Code.Rounded_Items.rounded_shapes import draw_rounded_rect


class Rounded_Item(tk.Frame):
    def __init__(self, parent, bg_colour, hover_colour, parent_bg_colour, text=None, command=None, font=None, fg_colour="white", width=170, height=42, radius=16):
        super().__init__(parent, bg=parent_bg_colour)

        self.width = width
        self.height = height
        self.radius = radius
        self.bg_colour = bg_colour
        self.hover_colour = bg_colour if hover_colour is None else hover_colour
        self.command = command

        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent_bg_colour, highlightthickness=0)
        self.canvas.pack()

        #If button text is inputted, a button is created else a frame is created
        self.content = None
        if text is not None:
            self.canvas.create_text(width / 2, height / 2, text=text, font=font, fill=fg_colour, width=width - 20)
        else:
            self.content = tk.Frame(self.canvas, bg=bg_colour)
            self.canvas.create_window(width / 2, height / 2, window=self.content, width=width - 20)

        self.set_colour(bg_colour)
        self.bind_children()

    #Draw the rounded shape and change its colour
    def set_colour(self, colour):
        self.canvas.delete("background")
        draw_rounded_rect(self.canvas, 0, 0, self.width, self.height, self.radius, colour, tag="background")
        self.canvas.tag_lower("background")

        if self.content is not None:
            self._colour_children(self.content, colour)

    #Change the background of widgets inside a card
    def _colour_children(self, widget, colour):
        try:
            widget.config(bg=colour)
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self._colour_children(child, colour)

    #Make the button/card and its child widgets clickable and hoverable
    def bind_children(self):
        #Function that actually binds the action to the button/card
        def bind(widget):
            if self.command is not None:
                widget.bind("<Button-1>", lambda e: self.command())
            widget.bind("<Enter>", lambda e: self.set_colour(self.hover_colour))
            widget.bind("<Leave>", lambda e: self.set_colour(self.bg_colour))

            for child in widget.winfo_children():
                bind(child)

        bind(self)