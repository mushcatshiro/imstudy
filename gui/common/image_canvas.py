import tkinter as tk
from PIL import ImageGrab, ImageTk, Image

class ImDisplayCanvas:
    def __init__(self, root: tk.Tk, fabspath):
        self.root = root
        with Image.open(fabspath) as im:
            image = ImageTk.PhotoImage(im)
            width, height = im.size

        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.create_image(0,0,image=image, anchor="nw")
        
        # canvas.pack()
        
        # canvas.bind("<Button 1>", getorigin)

def create_im_display_canvas(root, imdisp,  fabspath):
    imdisp = ImDisplayCanvas(root, fabspath)
    imdisp.grid(column=2, row=0, sticky='nswe')
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)