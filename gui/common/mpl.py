import tkinter as tk
import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.figure import Figure


class MplCanvas:
    """
    source: https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
    """
    def __init__(self, root: tk.Tk, title: str, fig: Figure):
        self.root = root
        self.root.wm_title(title)
        self.fig = fig
        # ax = self.fig.add_subplot()  # preadded prior to passing to this class
        # line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
        # ax.set_xlabel("time [s]")
        # ax.set_ylabel("f(t)")

        self.canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        # canvas.mpl_connect(
        #     "key_press_event", lambda event: print(f"you pressed {event.key}")
        # )
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        # button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        # button_quit.pack(side=tkinter.BOTTOM)
        # slider_update.pack(side=tkinter.BOTTOM)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def register_function(self, func):
        self.canvas.mpl_connect("key_press_event", func)


# def update_frequency(new_val):
#     # retrieve frequency
#     f = float(new_val)

#     # update data
#     y = 2 * np.sin(2 * np.pi * f * t)
#     line.set_data(t, y)

#     # required to update canvas and attached toolbar!
#     canvas.draw()


# slider_update = tkinter.Scale(
#     root, from_=1, to=5, orient=tkinter.HORIZONTAL, command=update_frequency, label="Frequency [Hz]"
# )

