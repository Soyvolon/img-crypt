import os
import tkinter.ttk as ttk
import tkinter as tk

from .ImagePreviewFrame import ImagePreviewFrame
from .AppFrameInterface import AppFrameInterface
from Core.Services import ProfileManagementServiceInterface as PMSI

class UserSettingsFrame(AppFrameInterface):
    def __init__(self, parent, services):
        # initialize the user settings frame object
        ttk.LabelFrame.__init__(self,
            master=parent,
            height=150,
            text="User Settings"
        )

        # Save the service collection
        self.__services = services
        
        self.__initialized = False

        self.__addImage = tk.PhotoImage(file=os.path.abspath(os.path.join('icon', 'add_circle_gfont.png')))
        self.__deleteImage = tk.PhotoImage(file=os.path.abspath(os.path.join('icon', 'delete_forever_gfont.png')))
        self.__saveImage = tk.PhotoImage(file=os.path.abspath(os.path.join('icon', 'save_gfont.png')))

        self._build()

    def initialize(self) -> None:
        # get the services we need
        self.__imagePreview: ImagePreviewFrame = self.__services[ImagePreviewFrame]
        self.__profileService: PMSI = self.__services[PMSI]

        self.__initialized = True  
        # we dont need the whole service collection
        self.__services = None      

    def _build(self):
        # left frame
        self.__leftFrame = ttk.Frame(
            master=self,
            padding=(2, 2, 6, 2)
        )

        # ---- items on the left of the menu ----

        # user profile frame
        self.__userProfileFrame = ttk.Frame(
            master=self.__leftFrame
        )

        # user profile label
        self.__userProfileLabel = ttk.Label(
            master=self.__leftFrame,
            text="User Profiles"
        )

        # user profile selection
        self.__userProfile = ttk.Combobox(
            master=self.__userProfileFrame
        )

        # user profile add button
        self.__addUserProfile = ttk.Button(
            master=self.__userProfileFrame,
            image=self.__addImage
        )

        # user profile delete button
        self.__deleteUserProfile = ttk.Button(
            master=self.__userProfileFrame,
            image=self.__deleteImage
        )

        # color settings label
        self.__colorSettingsLabel = ttk.Label(
            master=self.__leftFrame,
            text="Color Settings"
        )

        # color settings combo
        self.__colorSettings = ttk.Combobox(
            master=self.__leftFrame,
            values=('Standard', 'Unique')
        )
        
        # characters per pixel label
        self.__charsPerPixelLabel = ttk.Label(
            master=self.__leftFrame,
            text="Characters Per Pixel"
        )

        # characters per pixel combo
        self.__charsPerPixel = ttk.Combobox(
            master=self.__leftFrame,
            values=('1', '2', '3')
        )

        # ---- end left frame code ----

        # ---- Items on the right of the settings pane ----
        # right frame
        self.__rightFrame = ttk.Frame(
            master=self,
            padding=(6, 2, 2, 2)
        )

        # settings profile name
        self.__settingsProfileFrame = ttk.Frame(
            master=self.__rightFrame
        )

        # settings profile label
        self.__settingsProfileLabel = ttk.Label(
            master=self.__rightFrame,
            text="Settings Profiles"
        )

        # settings profile selection
        self.__settingsProfile = ttk.Combobox(
            master=self.__settingsProfileFrame
        )

        # settings profile add button
        self.__addSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__addImage
        )

        # settings profile delete button
        self.__deleteSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__deleteImage
        )

        # settings profile save button
        self.__saveSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__saveImage
        )

        # pixel spacing label
        self.__pixelSpacingLabel = ttk.Label(
            master=self.__rightFrame,
            text="Pixel Spacing"
        )

        vcmd = (self.register(self.validate_number), '%P')

        # pixel spacing input
        self.__pixelSpacing = ttk.Entry(
            master=self.__rightFrame,
            validate='key',
            validatecommand=vcmd
        )

        # hash key label
        self.__hashKeyLabel = ttk.Label(
            master=self.__rightFrame,
            text="Hash Key"
        )

        # hash key input
        self.__hashKey = ttk.Entry(
            master=self.__rightFrame,
            show='*'
        )

        # ---- end right frame code ----

    def pack_ui(self):
        # configure the row/column weights
        self.columnconfigure(tuple(range(2)), weight=1, pad=4)
        self.rowconfigure(tuple(range(1)), weight=1, pad=4)

        # setup the columns for the frames
        self.__leftFrame.grid(column=0, row=0, sticky='nswe', padx=2, pady=2)
        self.__rightFrame.grid(column=1, row=0, sticky='nswe', padx=2, pady=2)

        # ---- left grid ----
        # setup the gird weight
        self.__leftFrame.rowconfigure(tuple(range(5)), weight=1)
        self.__leftFrame.columnconfigure(0, weight=1)
        # setup all the items on the left side, rows 0 to 5
        self.__userProfileLabel.grid(column=0, row=0, sticky='nwe', padx=2, pady=2)
        self.__userProfileFrame.grid(column=0, row=1, sticky='nwe', padx=2, pady=2)
        self.__charsPerPixelLabel.grid(column=0, row=2, sticky='we', padx=2, pady=2)
        self.__charsPerPixel.grid(column=0, row=3, sticky='we', padx=2, pady=2)
        self.__colorSettingsLabel.grid(column=0, row=4, sticky='swe', padx=2, pady=2)
        self.__colorSettings.grid(column=0, row=5, sticky='swe', padx=2, pady=2)
            # ---- user profile frame ----
            # setup the grid weight
        self.__userProfileFrame.rowconfigure(0, weight=1)
        self.__userProfileFrame.columnconfigure(tuple(range(3)), weight=1)
            # setup the user profile selection/mod row
        self.__userProfile.grid(column=0, row=0, sticky='nwe', padx=2, pady=2)
        self.__addUserProfile.grid(column=1, row=0, sticky='nwe', padx=2, pady=2)
        self.__deleteUserProfile.grid(column=2, row=0, sticky='nwe', padx=2, pady=2)
            # ---- end user profile frame ----
        # ---- end left grid ----

        # ---- right grid ----
        # setup the grid weight
        self.__rightFrame.rowconfigure(tuple(range(5)), weight=1)
        self.__rightFrame.columnconfigure(0, weight=1)
        # setup all the items on the right side, rows 0 to 5
        self.__settingsProfileLabel.grid(column=0, row=0, sticky='nwe', padx=2, pady=2)
        self.__settingsProfileFrame.grid(column=0, row=1, sticky='nwe', padx=2, pady=2)
        self.__pixelSpacingLabel.grid(column=0, row=2, sticky='we', padx=2, pady=2)
        self.__pixelSpacing.grid(column=0, row=3, sticky='we', padx=2, pady=2)
        self.__hashKeyLabel.grid(column=0, row=4, sticky='swe', padx=2, pady=2)
        self.__hashKey.grid(column=0, row=5, sticky='swe', padx=2, pady=2)
            # ---- settings profile frame ----
            # setup the grid weight
        self.__settingsProfileFrame.rowconfigure(0, weight=1)
        self.__settingsProfileFrame.columnconfigure(tuple(range(4)), weight=1)
            # setup the settings profile selection/mod row
        self.__settingsProfile.grid(column=0, row=0, sticky='nwe', padx=2, pady=2)
        self.__addSettingsProfile.grid(column=1, row=0, sticky='nwe', padx=2, pady=2)
        self.__deleteSettingsProfile.grid(column=2, row=0, sticky='nwe', padx=2, pady=2)
        self.__saveSettingsProfile.grid(column=3, row=0, sticky='nwe', padx=2, pady=2)
            # ---- end settings profile frame ----
        # ---- end right grid ----

    def validate_number(self, val: str) -> bool:
        """
        Validates input to verify that it is only a positive number

        Precondition:
            A user has inputted data into an input field

        Args:
            val (str): The new string value for the entry box

        Returns:
            bool: Returns True if the value is a valid, positive, number, or is empty

        Postcondition:
            A: The entry box reflects the new value
                OR
            B: The entry box remains the same as it was pre-input
        """
        if val == "" or val is None:
            return True

        try:
            return float(val) > 0
        except:
            return False