# Last Edit: 2022-10-28
# Author(s): Bounds

from email.policy import default
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk

import pathlib
import io
import os
import shutil

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

        self.__rawImage: pathlib.Path = None
        self.__previewImage: pathlib.Path = None
        self.__previewImageResized: Image = None

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
    def load_image(self) -> None:
        """Loads an image into the preview and registers the internal
        changes version for edit previews.

        If an image is already loaded this method will override that image.

        Precondition:
            None

        Args:
            None

        Returns:
            None

        Postcondition:
            A local copy of the image is kept by the application to use and edit.
                AND
            The original image is not modified.
        """
        self._error_if_not_initialized()
        try:
            # ask to open a file with the windows file picker
            with fd.askopenfile(mode='r', filetypes=[('Single Image', '.png'), ('Batch Images', '.gif')]) as ogImage:
                if ogImage:
                    # the image is loaded, so we are going to continue
                    # by getting the file path object
                    pathObj = pathlib.Path(ogImage.name)

                    # if the pathObj has a proper suffix
                    if pathObj.suffix == '.png' or pathObj.suffix == '.gif':
                        # we can load it.
                        # save the path object into the raw image variable
                        self.__rawImage = pathObj
                        # then we create our temp dir if its not there
                        os.makedirs('tmp', exist_ok=True)
                        # and then create the temp image file path for preview/modification
                        tmpImageName = f'preview_image{pathObj.suffix}'
                        self.__previewImage = pathlib.Path(os.path.join('tmp', tmpImageName))

                        # reset the preview file by copying the og to the preview
                        # location
                        self.__reset_preview_file()
                        # and finally update the image to its raw value
                        # by passing none
                        self.update_image(None, None)
                    else:
                        # if the format is bad, reset the raw image
                        self.__rawImage = None
                        # and preview image file paths
                        self.__previewImage = None
                        # and update the image, which will be set to
                        # blank as there is no image file
                        self.update_image(None, None)
                        # then show an error to the user.
                        mb.showerror(title="Image Load Error", 
                            message="A file of type .gif or .png was unable to be loaded.")
        except:
            # we dont do anything here because this only catches
            # an error if the file fails to open.
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

        # if we have a preview image
        if self.__previewImage:
            self.__create_image_object()
            self.__imageCanvas.create_image(0, 0, image=self.__previewImageObject, anchor='nw')
        pass

    def save_image(self) -> None:
        """Saves the currently loaded image, with all modifications, as
        a new file.

        Precondition:
            An image is loaded with load_image.

        Args:
            None

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

    def __reset_preview_file(self):
        """Resets the preview image file.

        Precondition:
            None
        
        Args:
            None

        Returns:
            None

        Postcondition:
            If both raw image and preview image are defined, the raw image is
            copied to preview image.
                OR
            No action is taken.
        """
        if self.__rawImage and self.__previewImage:
            # Copy the raw file to the preview file location.  
            shutil.copy(str(self.__rawImage), str(self.__previewImage))

    def __create_image_object(self):
        # if the raw image and preview image exist ...
        if self.__rawImage and self.__previewImage:
            # ... then open the preview image ...
            with Image.open(str(self.__previewImage)) as img:
                # ... and get the canvas size ...
                # self.__imageCanvas.update()
                canvx = self.__imageCanvas.winfo_width()
                canvy = self.__imageCanvas.winfo_height()
                ogx = img.width
                ogy = img.height

                ratio = 1
                if ogx >= ogy:
                    # larger width than height/equal height and width
                    ratio = canvx / ogx
                else:
                    # larger height than width
                    ratio = canvy / ogy

                x = int(ogx * ratio)
                y = int(ogy * ratio)

                # ... then resize the image and save the copy for later use ...
                self.__previewImageObject = ImageTk.PhotoImage(img.resize((x, y)))
        else:
            # ... otherwise get rid of the image data
            self.__previewImageObject = None

    # END REGION