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
from PIL import Image, ImageTk


SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png')

class FilesNav:
    def __init__(self):
        self.top_dir = None
        self.files = []
        self.index = -1

    def update(self, top_dir, file=None):
        if self.files:
            self.files = []
            self.index = -1
        self.top_dir = top_dir
        if file is not None:
            self.files.append(file)
            return
        for file in os.listdir(top_dir):
            if file.lower().endswith(SUPPORTED_IMAGE_FORMATS):
                self.files.append(file)
        return

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
    def __init__(self, root, main_app):
        super().__init__(root)
        self.root = root
        self.main_app = main_app
        self.open_file_button = tk.Button(self, text="Open File", command=self.open_file)
        self.open_dir_button = tk.Button(self, text="Open Directory", command=self.open_dir)
        self.next_image_button = tk.Button(self, text="Next Image", command=self.next_image)
        self.prev_image_button = tk.Button(self, text="Previous Image", command=self.prev_image)
        self.open_file_button.grid()
        self.open_dir_button.grid()
        self.next_image_button.grid()
        self.prev_image_button.grid()
        self.grid()
        
    def open_file(self):
        abs_fpath = filedialog.askopenfilename()
        # separate root path and file name
        top_dir, fname = os.path.split(abs_fpath)
        file_nav.update(top_dir, fname)

    def open_dir(self):
        top_dir = filedialog.askdirectory()
        file_nav.update(top_dir)
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

def on_click(event):
    """
    to support
    - [ ] line (2 clicks, force straight or freehand)
    - [ ] rectangle (2 clicks or 4 click)
    - [ ] circle (3 clicks)
    """
    print(event.xdata, event.ydata)

class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


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
        print(self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight())
        # self.canvas = ResizingCanvas(self.root)
        self.canvas.grid(row=1, column=0, sticky='nsew')
    
    def create_widgets(self):
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid()

    def _process_image(self, top_dir, fname):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid()
        im = Image.open(os.path.join(top_dir, fname))
        image = ImageTk.PhotoImage(im)
        fig = Figure(dpi=200)  # make option
        fig.add_subplot(111).imshow(im)
        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.canvas, pack_toolbar=False)
        self.toolbar.update()
        self.fig_canvas.mpl_connect("key_press_event", key_press_handler)
        self.fig_canvas.mpl_connect("button_press_event", on_click)
        self.toolbar.pack()
        self.fig_canvas.get_tk_widget().pack(expand=True)

    def process_next_image(self, top_dir, fname):
        self._process_image(top_dir, fname)

    def process_prev_image(self, top_dir, fname):
        self._process_image(top_dir, fname)

    def switch_frame(self, frame_class):
        # grid_config = frame_class.grid_config()
        new_frame = frame_class(self.root)
        if self._frame:
            self._frame.destroy()
        self._frame = new_frame
        # self.root.
        # self._frame.grid()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.start()