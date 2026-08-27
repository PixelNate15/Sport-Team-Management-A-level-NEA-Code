from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def draw_graph(parent_frame, x_points, y_points, graph_title, x_title, y_title, row=0, column=0, want_integer_x_axis = False):     
    figure = Figure(figsize=(4,3.2), dpi=100)
    graph = figure.add_subplot(1,1,1)
    
    graph.plot(x_points, y_points, marker="o")
    
    graph.set_title(graph_title)
    graph.set_xlabel(x_title)
    graph.set_ylabel(y_title)
    
    graph.tick_params(axis="x", labelrotation=90)
    figure.subplots_adjust(left=0.16, right=0.95, top=0.85, bottom=0.30)
    if want_integer_x_axis == True:
        graph.set_xticks(x_points)
    
    canvas = FigureCanvasTkAgg(figure, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, sticky="nsew", padx=10, pady=10)

    return canvas