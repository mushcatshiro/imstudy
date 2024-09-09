import tkinter as tk
import tkinter.font

from imlabel.imlabelframe import ImLabelFrame

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        # self.customFont = tkinter.font.Font(family="Helvetica", size=40)
        self.root = root
        self._frame = None
        self.grid()
        # self.create_widgets()
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.switch_frame(ImLabelFrame))
        # file_menu.add_command(label="New2", command=lambda: self.switch_frame(PageTwo))
    
    def create_widgets(self):
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.root)
        if self._frame:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


if __name__ == "__main__":
    root = tk.Tk()
    # root.tk.call('tk', 'scaling', 3.0)
    app = MainApplication(root=root)
    app.master.title("Sample Application")
    root.state("zoomed")
    app.mainloop()