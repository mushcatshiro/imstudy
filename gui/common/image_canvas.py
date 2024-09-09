import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageGrab, ImageTk, Image

class ImDisplayCanvas:
    def __init__(self, root: tk.Tk, fabspath):
        # super().__init__(root)
        self.root = root
        # self.grid()
        with Image.open(fabspath) as im:
            # im = im.resize((400, 400))
            self.image = ImageTk.PhotoImage(im)
            width, height = im.size

        # self.canvas = tk.Canvas(root, width=width, height=height)
        # self.canvas.create_image(0,0,image=image, anchor="nw")
        self.label = ttk.Label(self, image=self.image)
        # self.label.grid(column=0, row=0, sticky='ne')
        # self.root.grid_columnconfigure(1, weight=4)
        # self.root.grid_rowconfigure(0, weight=0)
        
        # canvas.pack()
        
        # canvas.bind("<Button 1>", getorigin)

def create_im_display_canvas(root, imdisp,  fabspath):
    imdisp = ImDisplayCanvas(root, fabspath)
    imdisp.grid(column=2, row=0, sticky='nswe')
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)