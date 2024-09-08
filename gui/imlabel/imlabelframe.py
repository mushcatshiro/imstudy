import tkinter as tk


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