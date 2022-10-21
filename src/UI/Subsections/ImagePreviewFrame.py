import tkinter as tk
import tkinter.ttk as ttk
from .AppFrameInterface import AppFrameInterface

class ImagePreviewFrame(AppFrameInterface):
    def __init__(self, parent):
        # initialize the preview frame object
        tk.LabelFrame.__init__(self,
            master=parent,
            borderwidth=1,
            #bg="yellow", 
            height=500,
            width=500,
            text="Image Preview"
        )

        self._initialize()
        
    def _initialize(self):
        self.__imageCanvas = tk.Canvas(
            master=self,
            background='gray75',
            width=500,
            height=500
        )

    def pack_ui(self):
        # configure the row/cols to grow
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # stick the canvas on the grid
        self.__imageCanvas.grid(row=0, column=0, padx=2, pady=2, sticky='nswe')