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

from .AppFrameInterface import AppFrameInterface
from Core.Data import SettingsProfile
from Core.Error import ImageProcessingError

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
        from .UserSettingsFrame import UserSettingsFrame
        from .UserInputFrame import UserInputFrame
        from Core.Services import ImageModificationServiceInterface as IMSI

        self.__imageService: IMSI = self.__services[IMSI]
        self.__inputFrame: UserInputFrame = self.__services[UserInputFrame]
        self.__settingFrame: UserSettingsFrame = self.__services[UserSettingsFrame]

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
        # TODO this needs to be updated to support detecting if an image 
        # has hidden text and either loading it for preview/results 
        # depending on the situation. Should move existing code
        # to a new method and let this public method handle just
        # detection and routing to the proper private method to either
        # load preview or load file data.
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
            
            # ... if the path object exists ...
            if pathObj:
                # ... try and get the header from the image ...
                profile = self.__imageService.get_header(str(pathObj))
                # ... and set the hidden text flag ...
                load_hidden_text = False
                # ... if the profile exists ...
                if profile:
                    # ... the ask if the user wants to load hidden text ...
                    res = mb.askyesnocancel("Load Image", "Load hidden text from this image?")
                    # ... and if res is not None
                    if res != None:
                        # ... set load to the response of the prompt ...
                        load_hidden_text = res
                    else:
                        # ... if res is none, exit the method without doing
                        # anything ...
                        return

                # ... and if the user wants to load hidden text ...
                if load_hidden_text:
                    # ... load that text ...
                    self.__load_image_for_revealing(pathObj, profile)
                else:
                    # ... otherwise, load the image for hiding ...
                    self.__load_image_for_hiding(pathObj)
        except:
            mb.showerror('Error', "An unexpected error occurred when trying \
            to load the selected file.")
        
    def __load_image_for_hiding(self, pathObj: pathlib.Path):
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
            self.update_image()
        else:
            self.clear_image()
            # then show an error to the user.
            mb.showerror(title="Image Load Error", 
                message="A file of type .gif or .png was unable to be loaded.")

    def __load_image_for_revealing(self, pathObj: pathlib.Path, profile: SettingsProfile):
        pass

    def update_image(self, suppressErrors: bool = True) -> None:
        """Update the currently loaded image with the
        provided settings profile

        Precondition:
            An image is loaded with load_image.

        Args:
            None

        Returns:
            None

        Postcondition:
            The preview image is updated to match the new settings/text.
        """
        self._error_if_not_initialized()

        # try to get the active profile
        curText = self.__inputFrame.get_current_text()

        # try to get the existing text
        curSettings = self.__settingFrame.get_current_settings()

        # then, if we have active settings,
        # run it through the image service.
        if curSettings:
            try:
                self.__imageService.hide_text_in_image(curSettings, curText, 
                    str(self.__rawImage), str(self.__previewImage))
            except ImageProcessingError as ipe:
                if (not suppressErrors):
                    mb.showerror("Image Processing Error", ipe.message)
                return
            except:
                mb.showerror("Image Processing Error", f'Failed to hide text in image. An unknown error occurred.')
                self.clear_image()
                return

        self.__create_image_object()
        # make sure an image object was created
        if self.__previewImageObject:
            # and add it to the canvas
            self.__imageCanvas.create_image(0, 0, image=self.__previewImageObject, anchor='nw')
        else:
            # otherwise, get rid of all data
            self.clear_image()

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

        self.update_image(False)

        if self.__previewImage:
            fileType = self.__previewImage.suffix
            path = fd.asksaveasfilename(filetypes=[("Source Type", fileType)])
            with Image.open(self.__previewImage) as prev:
                if not path.endswith(fileType):
                    path += fileType
                prev.save(path)
                mb.showinfo('', 'File Saved Successfully.')
                self.clear_image()

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
        self.__previewImage = None
        self.__rawImage = None
        self.__create_image_object()
        self.__imageCanvas.delete('all')
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
        """Creates the image object to display as it needs to be resized.

        Precondition:
            The preview image has been created.

        Args:
            None

        Returns:
            None

        Postcondition:
            The image object is a copy of the preview image, resized to fit the display
            canvas while keeping its aspect ratio.
        """
        # if the preview image exists ...
        if self.__previewImage:
            # ... then open the preview image ...
            with Image.open(str(self.__previewImage)) as img:
                # ... and get the canvas size ...
                # self.__imageCanvas.update()
                canvx = self.__imageCanvas.winfo_width()
                canvy = self.__imageCanvas.winfo_height()
                # ... then the image size ...
                ogx = img.width
                ogy = img.height

                # ... then find the adjustment ratio to make it fit ...
                ratio = 1
                if ogx >= ogy:
                    # larger width than height/equal height and width
                    ratio = canvx / ogx
                else:
                    # larger height than width
                    ratio = canvy / ogy

                # ... then get the final size values ...
                x = int(ogx * ratio)
                y = int(ogy * ratio)

                # ... then resize the image and save the copy for later use ...
                self.__previewImageObject = ImageTk.PhotoImage(img.resize((x, y)))
        else:
            # ... otherwise get rid of the image data
            self.__previewImageObject = None

    # END REGION