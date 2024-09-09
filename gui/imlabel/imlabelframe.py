import tkinter as tk
from common.mpl import MplCanvas
from common.directory_tree import create_tree
from common.image_canvas import ImDisplayCanvas, create_im_display_canvas

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
        tk.Frame.__init__(self, root)
        self.root = root

        self.directory_vsb = None
        self.directory_hsb = None
        self.directory_tree = None
        create_tree(
            self.root,
            self.directory_vsb,
            self.directory_hsb,
            self.directory_tree
        )

        self.form_pane = None
        # self.image_pane = ImDisplayCanvas(self.root)
        self.im_pane = None
        create_im_display_canvas(
            self.root,
            self.im_pane,
            r""
        )

    def execute_command(self):
        pass
