import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.font
import os
import glob
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import cv2
from mpl_interactions import ioff, panhandler, zoom_factory
import numpy as np


SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png')

class FilesNav:
    def __init__(self):
        self.top_dir = None
        self.files = []
        self.index = -1

    def update(self, top_dir, file=None, excl_suffixes=[]):
        if self.files:
            self.files = []
            self.index = -1
        self.top_dir = top_dir
        if file is not None:
            self.files.append(file)
            return
        for file in os.listdir(top_dir):
            file: str
            if not file.lower().endswith(SUPPORTED_IMAGE_FORMATS):
                continue
            if excl_suffixes and file.endswith(excl_suffixes):
                continue
            self.files.append(file)
        return

    def current(self):
        if self.index < 0 or self.index >= len(self.files):
            return None
        return (self.top_dir, self.files[self.index])

    def next(self):
        if self.index < len(self.files):
            self.index += 1
            return (self.top_dir, self.files[self.index])
        return None

    def prev(self):
        if self.index - 1 < 0:  # 0
            return None
        self.index -= 1
        return (self.top_dir, self.files[self.index])

file_nav = FilesNav()

class Toolbar(tk.Frame):
    def __init__(self, root, main_app, excl_suffix=None):
        super().__init__(root)
        self.root = root
        self.main_app = main_app
        self.open_file_button = tk.Button(self, text="Open File", command=self.open_file)
        self.open_dir_button = tk.Button(self, text="Open Directory", command=self.open_dir)
        self.next_image_button = tk.Button(self, text="Next Image", command=self.next_image)
        self.prev_image_button = tk.Button(self, text="Previous Image", command=self.prev_image)
        self.reload_button = tk.Button(self, text="Reload Image", command=self.reload_image)
        self.open_file_button.grid(row=0, column=0)
        self.open_dir_button.grid(row=0, column=1)
        self.next_image_button.grid(row=0, column=2)
        self.prev_image_button.grid(row=0, column=3)
        self.reload_button.grid(row=0, column=4)
        self.excl_suffix = excl_suffix
        self.grid()
        
    def open_file(self):
        abs_fpath = filedialog.askopenfilename()
        # separate root path and file name
        top_dir, fname = os.path.split(abs_fpath)
        file_nav.update(top_dir, fname)

    def open_dir(self):
        top_dir = filedialog.askdirectory()
        file_nav.update(top_dir, excl_suffix=self.excl_suffix)
        print("Top dir: ", file_nav.top_dir)
        print("Files: ", file_nav.files)

    def next_image(self):
        rv = file_nav.next()
        if rv is not None:
            self.main_app.process_next_image(*rv)
        else:
            print("No more images in directory")

    def prev_image(self):
        rv = file_nav.prev()
        if rv is not None:
            self.main_app.process_prev_image(*rv)
        else:
            print("No more images in directory")

    def reload_image(self):
        rv = file_nav.current()
        if rv is not None:
            self.main_app.process_reload_image(*rv)

def on_click(event):
    """
    to support
    - [ ] line (2 clicks, force straight or freehand)
    - [ ] rectangle (2 clicks or 4 click)
    - [ ] circle (3 clicks)
    """
    print(event.xdata, event.ydata)

class MainApplication:
    def __init__(self, *args, **kwargs):
        # tk.Frame.__init__(self, root, *args, **kwargs)
        # self.customFont = tkinter.font.Font(family="Helvetica", size=40)
        self.root = tk.Tk()
        self.root.title("Sample Application")
        self.root.state("zoomed")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # root.tk.call('tk', 'scaling', 3.0)
        self._frame = None
        self.root.bind("q", lambda e: self.root.quit())
        self.toolbar = Toolbar(self.root, self)
        # self.canvas = None
        self.canvas = tk.Canvas(self.root, bg='red')
        # self.canvas = ResizingCanvas(self.root)
        self.canvas.grid(row=1, column=0, sticky='nsew')

    def _process_image(self, top_dir, fname, xdata=None, ydata=None):
        self.top_dir = top_dir
        self.fname = fname
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid()
        im = cv2.imread(os.path.join(top_dir, fname))
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im[:1350, :, :]
        xlen, ylen = im.shape[1], im.shape[0]
        # fig = Figure((10, 6), dpi=200)  # make option
        with plt.ioff():
            fig, ax = plt.subplots((2, 1), figsize=(15, 15), dpi=200)
        ax[0].imshow(im)
        ax[1].imshow()
        ax[0].set_title(fname)
        # if xdata is not None and ydata is not None:
        #     ax.plot([x for x in range(xlen)], [ydata] * xlen, color="firebrick" if not emphasize else "k")
        self.disconnect_zoom = zoom_factory(ax)
        self.pan_handler = panhandler(fig)
        # fig.add_subplot(111).imshow(im)
        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.canvas, pack_toolbar=False)
        self.toolbar.update()
        self.fig_canvas.mpl_connect("key_press_event", key_press_handler)
        # self.fig_canvas.mpl_connect("button_press_event", self.fig_canvas_on_click)
        self.toolbar.pack()
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # self.fig_canvas.bind("<MouseWheel>", self.do_zoom)
        # self.fig_canvas.mpl_connect("scroll_event", self.do_zoom)

    def fig_canvas_on_click(self, event):
        self._process_image(self.top_dir, self.fname, event.xdata, event.ydata)

    def process_next_image(self, top_dir, fname):
        self._process_image(top_dir, fname)

    def process_prev_image(self, top_dir, fname):
        self._process_image(top_dir, fname)

    def process_reload_image(self, top_dir, fname):
        self._process_image(top_dir, fname)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.start()