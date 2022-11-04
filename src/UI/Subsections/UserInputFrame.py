# Last Edit: 2022-10-28
# Author(s): Bounds

from tkinter import Text
import tkinter.ttk as ttk
from tkinter import filedialog as fd

from .AppFrameInterface import AppFrameInterface

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

        self._build()
        
    def initialize(self) -> None:
        # get the services we need.
        from .UserSettingsFrame import UserSettingsFrame
        from .ImagePreviewFrame import ImagePreviewFrame
        
        self.__imagePreview: ImagePreviewFrame = self.__services[ImagePreviewFrame]
        self.__userSettings: UserSettingsFrame = self.__services[UserSettingsFrame]

        # register UI events
        self.__textInput.bind('<KeyPress>', self.__validate_text_input)
        self.__textInput.bind('<KeyRelease>', self.__validate_text_input)

        self.__initialized = True
        # we dont need this entire collection in memory anymore.
        self.__services = None

    def _error_if_not_initialized(self) -> None:
        if not self.__initialized:
            raise Exception("Frame Not Initialized")
    
    def _build(self) -> None:
        # text input field
        self.__textInput = Text(
            master=self,
            height=5
        )

        # button container
        self.__buttonFrame = ttk.Frame(
            master=self
        )

        # load image button
        self.__loadImage = ttk.Button(
            master=self.__buttonFrame,
            text="Load Image",
            width=7,
            command=self.__load_image_pressed
        )

        # save image button
        self.__saveImage = ttk.Button(
            master=self.__buttonFrame,
            text="Save Image",
            width=7,
            command=self.__save_image_pressed
        )

        # load text button
        self.__loadText = ttk.Button(
            master=self.__buttonFrame,
            text="Load Text",
            width=2,
            command=self.__load_text_pressed
        )

        # save text button
        self.__saveText = ttk.Button(
            master=self.__buttonFrame,
            text="Save Text",
            width=2,
            command=self.__save_text_pressed
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

    def get_current_text(self) -> str:
        """Gets the current text in the input box.

        Precondition:
            This frame is initialize
            
        Args:
            None

        Returns:
            (str): The current text

        Postcondition:
            The returned value matches the inputted text.
        """
        self._error_if_not_initialized()
        return self.__textInput.get('1.0', 'end')[:-1]

    def __validate_text_input(self, event) -> None:
        """
        Validate new text input into the user input text box

        Preconditions:
            The UI has been initialized and packed

        Args:
            event: The event that was called by the text input

        Returns:
            None

        Postcondition:
            The text box has only ASCII text in it
        """
        curText = self.get_current_text()
        if not curText.isascii():
            # get the rows of text
            curTextRows = curText.splitlines(True)
            # for each row, and each char, if the char is not unicode, save the row and col pos where row
            # starts at index 1.
            badChars = [
                # row, col
                (x + 1, y)
                # for each row ...
                for x in range(0, len(curTextRows)) 
                    # ... and each char in the row ...
                    for y in range(0, len(curTextRows[x]))
                        # ... if the value is not ASCII, save it ...
                        if ord(curTextRows[x][y]) >= 128]
            # ... then for each bad char...
            for pair in badChars:
                # ... delete it from the text box.
                self.__textInput.delete(f'{pair[0]}.{pair[1]}', f'{pair[0]}.{pair[1] + 1}')

    def __load_image_pressed(self):
        self._error_if_not_initialized()
        self.__imagePreview.load_image()
        pass

    def __save_image_pressed(self):
        self._error_if_not_initialized()
        self.__imagePreview.save_image()
        pass

    def __load_text_pressed(self):
        self._error_if_not_initialized()
        pass

    def __save_text_pressed(self):
        self._error_if_not_initialized()
        pass
