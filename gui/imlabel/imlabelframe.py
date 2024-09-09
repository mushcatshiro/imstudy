import tkinter as tk
import tkinter.ttk as ttk
from common.mpl import MplCanvas
from common.directory_tree import (
    create_tree,
    autoscroll,
    update_tree,
    change_dir,
    populate_roots
)
from common.image_canvas import ImDisplayCanvas, create_im_display_canvas
from PIL import Image, ImageTk

"""
design

+--------------------------------+
|     |           2              |
|     |--------------------------|
|     |                          |
|  1  |           3              |
+-----+-+------------------------+

1 is a tree view of target directory
(can 1 be multiple views to allow user to config drawn line colors?)
2 is a view to display image information + get command for 3
3 is a canvas (mpl or tk) to display image + draw lines

data flow

from 1 -> 2 -> 3 through `CurrentImageFile` object

a counter to keep tracked labeled images
tools to help measure the images (draw lines)
zoom support?
save to db
load separate rgb channel
"""


class ImLabelFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        # self.grid()
        self.grid(column=0, row=0, sticky='nswe')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)

        self.root = root

        self.directory_vsb = None
        self.directory_hsb = None
        self.directory_tree = None
        self.directory_vsb = ttk.Scrollbar(orient="vertical")
        self.directory_hsb = ttk.Scrollbar(orient="horizontal")

        self.directory_tree = ttk.Treeview(
            columns=("fullpath", "type", "size"),
            displaycolumns="size",
            yscrollcommand=lambda f, l: autoscroll(self.directory_vsb, f, l),
            xscrollcommand=lambda f, l: autoscroll(self.directory_hsb, f, l)
        )

        self.directory_vsb['command'] = self.directory_tree.yview
        self.directory_hsb['command'] = self.directory_tree.xview

        self.directory_tree.heading("#0", text="Directory Structure", anchor='w')
        self.directory_tree.column("#0", stretch=1)
        self.directory_tree.heading("size", text="File Size", anchor='w')
        self.directory_tree.column("size", stretch=1)

        populate_roots(self.directory_tree)
        self.directory_tree.bind('<<TreeviewOpen>>', update_tree)
        self.directory_tree.bind('<Double-Button-1>', change_dir)

        self.directory_tree.grid(column=0, row=0, sticky='nswe')
        self.directory_vsb.grid(column=1, row=0, sticky='nw')
        self.directory_hsb.grid(column=0, row=1, sticky='ew')

        self.form_pane = None
        with Image.open(r"E:\datasets\mvtec\bottle\train\good\000.png") as im:
            # im = im.resize((400, 400))
            self.image = ImageTk.PhotoImage(im)
        self.image_pane = ttk.Label(
            self.root,
            image=self.image
        )
        # self.image_pane.grid()
        self.image_pane.grid(column=2, row=0, sticky='ne')
        # print("e")
        # self.grid_columnconfigure(0, weight=4)
        # self.grid_rowconfigure(0, weight=1)
        # self.im_pane = None
        # create_im_display_canvas(
        #     self.root,
        #     self.im_pane,
        #     r"E:\datasets\mvtec\bottle\train\good\000.png"
        # )

    @staticmethod
    def grid_config():
        return {
            "column": [[0, 1], [1, 4]],
            "row": 0,
        }

    def execute_command(self):
        pass
