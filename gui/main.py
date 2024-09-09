import tkinter as tk
import tkinter.font

from imlabel.imlabelframe import ImLabelFrame

class MainApplication:
    def __init__(self, *args, **kwargs):
        # tk.Frame.__init__(self, root, *args, **kwargs)
        # self.customFont = tkinter.font.Font(family="Helvetica", size=40)
        self.root = tk.Tk()
        self.root.title("Sample Application")
        self.root.state("zoomed")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # root.tk.call('tk', 'scaling', 3.0)
        self._frame = None
        # self.grid()
        # self.create_widgets()
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.switch_frame(ImLabelFrame))
        # file_menu.add_command(label="New2", command=lambda: self.switch_frame(PageTwo))
        self.root.bind("q", lambda e: self.root.quit())
    
    def create_widgets(self):
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid()

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