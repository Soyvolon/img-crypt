from tkinter import Text
import tkinter.ttk as ttk

from .ImagePreviewFrame import ImagePreviewFrame
from .AppFrameInterface import AppFrameInterface
from Core.Services import ImageModificationServiceInterface as IMSI

class UserInputFrame(AppFrameInterface):
    def __init__(self, parent, services):
        # initialize the user input frame object
        ttk.LabelFrame.__init__(self,
            master=parent,
            #bg="blue", 
            width=500,
            height=350,
            text="Image Text"
        )

        self.__services = services

        self.__initialized = False

        self._build()
        
    def initialize(self) -> None:
        # get the services we need.
        self.__imagePreview: ImagePreviewFrame = self.__services[ImagePreviewFrame]
        self.__imageService: IMSI = self.__services[IMSI]        

        self.__initialized = True
        # we dont need this entire collection in memory anymore.
        self.__services = None
    
    def _build(self) -> None:
        # text input field
        self.__textInput = Text(
            master=self,
            height=5
        )
        self.__textInput.bind('<KeyPress>', self.__validate_text_input)
        self.__textInput.bind('<KeyRelease>', self.__validate_text_input)

        # button container
        self.__buttonFrame = ttk.Frame(
            master=self
        )

        # load image button
        self.__loadImage = ttk.Button(
            master=self.__buttonFrame,
            text="Load Image",
            width=7
        )

        # save image button
        self.__saveImage = ttk.Button(
            master=self.__buttonFrame,
            text="Save Image",
            width=7
        )

        # load text button
        self.__loadText = ttk.Button(
            master=self.__buttonFrame,
            text="Load Text",
            width=2
        )

        # save text button
        self.__saveText = ttk.Button(
            master=self.__buttonFrame,
            text="Save Text",
            width=2
        )

    def pack_ui(self) -> None:
        # pack the child objects

        # configure the text input
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=9)
        self.__textInput.grid(column=0, row=0, sticky="nswe", padx=3, pady=3)

        # configure the button frame within the data frame
        self.rowconfigure(1, weight=1)
        self.__buttonFrame.grid(column=0, row=1, sticky="nswe")

        # configure the button frame row/columns
        self.__buttonFrame.columnconfigure(tuple(range(5)), weight=1)
        self.__buttonFrame.rowconfigure(tuple(range(2)), weight=1)

        # load image/text buttons
        self.__loadImage.grid(column=0, row=0, columnspan=4, sticky="nswe", padx=3, pady=3)
        self.__loadText.grid(column=4, row=0, sticky="nswe", padx=3, pady=3)

        # save image/text buttons
        self.__saveImage.grid(column=0, row=1, columnspan=4, sticky="nswe", padx=3, pady=3)
        self.__saveText.grid(column=4, row=1, sticky="nswe", padx=3, pady=3)

    def __validate_text_input(self, event) -> bool:
        """
        Validate new text input into the user input text box

        Preconditions:
            The UI has been initialized and packed

        Args:
            event: The event that was called by the text input

        Returns:
            bool: This value is True if newValue is valid input

        Postcondition:
            The text box has only ASCII text in it
        """
        pass
        # TODO figure something out with this - blegh