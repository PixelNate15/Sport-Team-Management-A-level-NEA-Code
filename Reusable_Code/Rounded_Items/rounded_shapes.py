import tkinter as tk

#Draw a rounded rectange onto a canvas
def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, fill_colour, tag=None):
    if tag:
        tags = (tag,)
    else:
        tags = ()

    #Create 4 corner arcs
    canvas.create_arc(x1, y1, (x1 + radius * 2), (y1 + radius * 2), start=90, extent=90, fill=fill_colour, outline=fill_colour, tags=tags) #top left corner
    canvas.create_arc((x2 - radius * 2), y1, x2, (y1 + radius * 2), start=0, extent=90, fill=fill_colour, outline=fill_colour, tags=tags) #top right corner
    canvas.create_arc(x1, (y2 - radius * 2), (x1 + radius * 2), y2, start=180, extent=90, fill=fill_colour, outline=fill_colour, tags=tags) #bottom left corner
    canvas.create_arc((x2 - radius * 2), (y2 - radius * 2), x2, y2, start=270, extent=90, fill=fill_colour, outline=fill_colour, tags=tags) #bottom right corner
    
    #Two rectangles fill in the straight edges between the corners
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=fill_colour, outline=fill_colour, tags=tags)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=fill_colour, outline=fill_colour, tags=tags)
