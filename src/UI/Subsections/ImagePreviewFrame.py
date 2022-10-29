import tkinter as tk
import tkinter.ttk as ttk

from Core.Data.SettingsProfile import SettingsProfile
from .AppFrameInterface import AppFrameInterface
from Core.Services import ImageModificationServiceInterface as IMSI

class ImagePreviewFrame(AppFrameInterface):
    def __init__(self, parent, services):
        # initialize the preview frame object
        tk.LabelFrame.__init__(self,
            master=parent,
            borderwidth=1,
            #bg="yellow", 
            height=500,
            width=500,
            text="Image Preview"
        )

        self.__initialized = False

        self.__services = services

        self._build()

    def initialize(self) -> None:
        # load services
        self.__imageService: IMSI = self.__services[IMSI]

        self.__initialized = True
        # dump the no-longer-needed service collection
        self.__services = None

    def _error_if_not_initialized(self) -> None:
        if not self.__initialized:
            raise Exception("Frame Not Initialized")
        
    def _build(self):
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

    # REGION Service Methods
    def load_image(self, filePath: str) -> None:
        """Loads an image into the preview and registers the internal
        changes version for edit previews.

        If an image is already loaded this method will override that image.

        Precondition:
            None

        Args:
            filePath (str): The file path to the image to load.

        Returns:
            None

        Postcondition:
            A local copy of the image is kept by the application to use and edit.
                AND
            The original image is not modified.
        """
        self._error_if_not_initialized()
        pass

    def update_image(self, profile: SettingsProfile, text: str) -> None:
        """Update the currently loaded image with the
        provided settings profile

        Precondition:
            An image is loaded with load_image.

        Args:
            profile (SettingsProfile): The settings profile that contains how
            the image will be modified.

            text (str): The text to use in the modification.

        Returns:
            None

        Postcondition:
            The preview image is updated to match the new settings/text.
        """
        self._error_if_not_initialized()
        pass

    def save_image(self, filePath: str) -> None:
        """Saves the currently loaded image, with all modifications, as
        a new file.

        Precondition:
            An image is loaded with load_image.

        Args:
            filePath (str): The file path of the new image.

        Returns:
            None

        Postcondition:
            The preview image is saved to the local disk at filePath.
        """
        self._error_if_not_initialized()
        pass

    def clear_image(self) -> None:
        """Clears the currently loaded image.
        
        Precondition:
            An image is loaded with load_image.

        Args:
            None

        Returns:
            None

        Postcondition:
            This class is cleared of all loaded image data
            and the preview is returned to a blank slate.
        """
        self._error_if_not_initialized()
        pass
    # END REGION