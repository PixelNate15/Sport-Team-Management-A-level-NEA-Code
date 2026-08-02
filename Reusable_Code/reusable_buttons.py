def add_hover(button, original_colour, hover_colour):
    button.bind("<Enter>", lambda e: button.config(bg=hover_colour))
    button.bind("<Leave>", lambda e: button.config(bg=original_colour))