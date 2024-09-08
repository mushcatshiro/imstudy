from PIL import Image


class CurrentImageFile:
    def __init__(self):
        """
        filename: str
          full path to the image file
        info: dict
          image info including size, dimension, bit depth
        command: str
          command to be executed
        
        TODO
        ----
        - [ ] db info for each command type
        """
        self.filename = None
        self.info = None
        self.command = None
        self.command_history = []

    def on_select(self, event):
        self.filename = event.widget.get(event.widget.curselection()[0])
        self.info = Image.open(self.filename)

    def set_command(self, command):
        self.command_history.append(self.command)
        self.command = command