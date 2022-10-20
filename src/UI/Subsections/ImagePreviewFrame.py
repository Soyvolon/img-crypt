import tkinter as ttk
from .AppFrameInterface import AppFrameInterface

class ImagePreviewFrame(AppFrameInterface):
    def __init__(self, parent):
        # initialize the preview frame object
        ttk.LabelFrame.__init__(self,
            master=parent,
            borderwidth=1,
            #bg="yellow", 
            height=500,
            width=300,
            text="Image Preview"
        )

        self._initialize()
        
    def _initialize(self):
        pass

    def pack_ui(self):
        pass
        # pack the child objects