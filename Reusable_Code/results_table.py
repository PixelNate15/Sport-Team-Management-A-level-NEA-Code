import tkinter as tk
from tkinter import ttk
import constants as c


class Result_Table(tk.Frame):
    def __init__(self, parent, players):
        super().__init__(parent, bg=c.LIGHT_BACKGROUND, highlightbackground=c.LIGHT_BORDER, highlightcolor=c.LIGHT_BORDER, highlightthickness=2, bd=0)

        players = players
        headings = ["#", "Players", "1 (Your Team)", "1 (Opponent)", "2 (Your Team)", "2 (Opponent)", "Champ tie\n(W / L / None)", "Total Sets"]

        # Even grid columns hold content; odd columns are visible vertical lines.
        widths = [45, 250, 90, 90, 90, 90, 145, 105]

        for index, width in enumerate(widths):
            self.grid_columnconfigure(index * 2, minsize=width, weight=1 if index == 1 else 0)
            if index < len(widths) - 1:
                self.grid_columnconfigure(index * 2 + 1, minsize=2)

        # Match the readonly player dropdowns in Add/Edit Fixture.
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("Result.TCombobox", fieldbackground=c.LIGHT_SIDEBAR, background=c.LIGHT_SIDEBAR, foreground=c.LIGHT_PRIMARY_ACCENT, arrowcolor=c.LIGHT_MAIN_TEXT, bordercolor=c.LIGHT_BORDER, lightcolor=c.LIGHT_SIDEBAR, darkcolor=c.LIGHT_SIDEBAR, selectbackground=c.LIGHT_SIDEBAR, selectforeground=c.LIGHT_PRIMARY_ACCENT)
        self.style.map("Result.TCombobox", fieldbackground=[("readonly", c.LIGHT_SIDEBAR)], foreground=[("readonly", c.LIGHT_PRIMARY_ACCENT)])
        self.option_add("*TCombobox*Listbox.background", c.LIGHT_SIDEBAR)
        self.option_add("*TCombobox*Listbox.foreground", c.LIGHT_MAIN_TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", c.LIGHT_PRIMARY_ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", "white")
        self.option_add("*TCombobox*Listbox.font", c.FONT_ENTRY)

        self.scores = []

        # Creates the header row
        for index, heading in enumerate(headings):
            self._cell(0, index, heading, header=True)

        #Creates the horizontal lines below the headers
        self._horizontal_line(1, thickness=2)

        #Creates the four match rows.
        for match_index in range(4):
            grid_row = 2 + match_index * 2
            self._cell(grid_row, 0, str(match_index + 1))
            self._cell(grid_row, 1, players[match_index] if match_index < len(players) else "")

            #Creates the score entry boxes
            row_vars = []

            for col in (2, 3, 4, 5):
                var = tk.StringVar()
                entry = tk.Entry(self, textvariable=var, font=c.FONT_ENTRY, bg=c.LIGHT_SIDEBAR, fg=c.LIGHT_PRIMARY_ACCENT, justify="center", width=6)
                entry.grid(row=grid_row, column=col * 2, padx=6, pady=12, sticky="ew")
                row_vars.append(var)

            #Creates the championship tie-break dropdown
            tie_var = tk.StringVar(value="None")
            tie = ttk.Combobox(self, textvariable=tie_var, values=("W", "L", "None"), state="readonly", width=8, justify="center", font=c.FONT_ENTRY, style="Result.TCombobox")
            tie.grid(row=grid_row, column=12, padx=8, pady=12, sticky="ew")

            #Creates the total sets label
            total_var = tk.StringVar(value="0 - 0")
            total = tk.Label(self, textvariable=total_var, font=c.FONT_LABEL_BOLD, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND)

            total.grid(row=grid_row, column=14, padx=4, pady=8, sticky="nsew")

            #Automatically recalculate totals when scores change
            for var in row_vars:
                var.trace_add("write", lambda *_args, values=row_vars, tie=tie_var, result=total_var: self._update_total(values, tie, result))

            tie_var.trace_add("write", lambda *_args, values=row_vars, tie=tie_var, result=total_var: self._update_total(values, tie, result))

            #Stores the variables for retrieving scores later
            self.scores.append({"sets": row_vars, "champ_tie": tie_var, "total_sets": total_var})

            #Horizontal line below each match
            self._horizontal_line(grid_row + 1, thickness=2)


        #Method to create full-height vertical dividing lines
        for divider in range(7):
            separator = tk.Frame(self, bg=c.LIGHT_BORDER, width=2)

            separator.grid(row=0, column=divider * 2 + 1, rowspan=10, sticky="ns")

    #Method to build the cells
    def _cell(self, row, column, text, header=False):
        label = tk.Label(self, text=text, font=c.FONT_LABEL_BOLD if header else c.FONT_LABEL, fg=c.LIGHT_MAIN_TEXT, bg=c.LIGHT_BACKGROUND, justify="center", anchor="center", padx=8, pady=14)
        label.grid(row=row, column=column * 2, sticky="nsew")
        return label

    def _horizontal_line(self, row, thickness=2):
        self.grid_rowconfigure(row, minsize=thickness)
        tk.Frame(self, bg=c.LIGHT_BORDER, height=thickness).grid(row=row, column=0, columnspan=15, sticky="ew")

    @staticmethod
    def _update_total(values, tie, result):
        home = away = 0

        for h, a in ((0, 1), (2, 3)):
            hs = values[h].get().strip()
            as_ = values[a].get().strip()

            if not (hs.isdigit() and as_.isdigit()):
                continue

            if int(hs) > int(as_):
                home += 1

            elif int(as_) > int(hs):
                away += 1

        if tie.get() == "W":
            home += 1

        elif tie.get() == "L":
            away += 1

        result.set(f"{home} - {away}")

    def get_scores(self):
        return [
            {
                "match": i + 1,
                "set_1_home": row["sets"][0].get(),
                "set_1_away": row["sets"][1].get(),
                "set_2_home": row["sets"][2].get(),
                "set_2_away": row["sets"][3].get(),
                "champ_tie": row["champ_tie"].get(),
                "total_sets": row["total_sets"].get()
            }
            for i, row in enumerate(self.scores)
        ]