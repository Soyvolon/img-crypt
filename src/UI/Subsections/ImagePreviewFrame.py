import tkinter as tk

class ImagePreviewFrame(tk.Frame):
    def __init__(self):
        # initialize the preview frame object
        tk.Frame.__init__(
            master=self,
            relief=tk.RAISED,
            borderwidth=1,
            #bg="yellow", 
            height=500,
            width=300
        )

        self.__initialize()
        
    def __initialize(self):
        pass