from tkinter import HORIZONTAL, VERTICAL
import tkinter.ttk as ttk
from wsgiref import validate
from .AppFrameInterface import AppFrameInterface

class UserSettingsFrame(AppFrameInterface):
    def __init__(self, parent):
        # initialize the user settings frame object
        ttk.LabelFrame.__init__(self,
            master=parent,
            height=250,
            text="User Settings"
        )

        self._initialize()
        
    def _initialize(self):
        # user profile label
        self.__userProfileLabel = ttk.Label(
            master=self,
            text="User Profiles"
        )

        # user profile selection
        self.__userProfile = ttk.Combobox(
            master=self
        )

        # user profile add button
        self.__addUserProfile = ttk.Button(
            master=self
        )

        # user profile delete button
        self.__deleteUserProfile = ttk.Button(
            master=self
        )

        # settings profile label
        self.__settingsProfileLabel = ttk.Label(
            master=self,
            text="Settings Profiles"
        )

        # settings profile selection
        self.__settingsProfile = ttk.Combobox(
            master=self
        )

        # settings profile add button
        self.__addSettingsProfile = ttk.Button(
            master=self
        )

        # settings profile delete button
        self.__deleteSettingsProfile = ttk.Button(
            master=self
        )

        # settings profile save button
        self.__saveSettingsProfile = ttk.Button(
            master=self
        )

        # characters per pixel label
        self.__charsPerPixelLabel = ttk.Label(
            master=self,
            text="Characters Per Pixel"
        )

        # characters per pixel combo
        self.__charsPerPixel = ttk.Combobox(
            master=self,
            values=('1', '2', '3')
        )

        # pixel spacing label
        self.__pixelSpacingLabel = ttk.Label(
            master=self,
            text="Pixel Spacing"
        )

        vcmd = (self.register(self.validate_number), '%P')

        # pixel spacing input
        self.__pixelSpacing = ttk.Entry(
            master=self,
            validate='key',
            validatecommand=vcmd
        )

        # color settings label
        self.__colorSettingsLabel = ttk.Label(
            master=self,
            text="Color Settings"
        )

        # color settings combo
        self.__colorSettings = ttk.Combobox(
            master=self,
            values=('Standard', 'Unique')
        )

        # hash key label
        self.__hashKeyLabel = ttk.Label(
            master=self,
            text="Hash Key"
        )

        # hash key input
        self.__hashKey = ttk.Entry(
            master=self,
            show='*'
        )

        # spacer frames
        self.__vertSpacerA = ttk.Separator(
            master=self,
            orient=HORIZONTAL
        )
        self.__vertSpacerB = ttk.Separator(
            master=self,
            orient=HORIZONTAL
        )
        self.__horizSpacer = ttk.Separator(
            master=self,
            orient=VERTICAL
        )

    def pack_ui(self):
        # pack the grid!
        # 7 rows, 12 cols        1 1
        #    0 1 2 3 4 5 6 7 8 9 0 1
        #   |-----------------------|
        # 0 | A       | | | B       | A: user profile label, B: settings profile label
        #   |-----------------------|
        # 1 | A   |B|C| | | D |E|F|G| A: user profile, B: user new, C: user del, D: setting profile, E: setting new, F: setting del, G: setting save
        #   |-----------------------|
        # 2 | | | | | | | | | | | | | Nothing in this row
        #   |-----------------------|
        # 3 | A       |   | B       | A: CharPerPixel label, B: pixel spacing label
        #   |-----------------------|
        # 4 | A       |   | B       | A: CharPerPixel combo, B: pixel spacing entry
        #   |-----------------------|
        # 5 | A       |   | B       | A: color settings label, B: hash key label
        #   |-----------------------|
        # 6 | A       |   | B       | A: color settings combo, B: hash key entry
        #   |-----------------------|

        # configure the row/column weights
        self.columnconfigure(tuple(range(12)), weight=1)
        self.rowconfigure(tuple(range(7)), weight=1)

        # setup row 0
        self.__userProfileLabel.grid(column=0, row=0, columnspan=5)
        self.__settingsProfileLabel.grid(column=7, row=0, columnspan=5)

        # setup row 1
        self.__userProfile.grid(column=0, row=1, columnspan=3)
        self.__addUserProfile.grid(column=4, row=1)
        self.__deleteUserProfile.grid(column=5, row=1)
        
        self.__settingsProfile.grid(column=7, row=1, columnspan=2)
        self.__addSettingsProfile.grid(column=9, row=1)
        self.__deleteSettingsProfile.grid(column=10, row=1)
        self.__saveSettingsProfile.grid(column=11, row=1)

        # setup spacers on row 2/mid cols
        self.__vertSpacerA.grid(column=0, row=2, columnspan=5)
        self.__vertSpacerB.grid(column=7, row=2, columnspan=5)
        self.__horizSpacer.grid(column=5, row=0, columnspan=2, rowspan=7)

        # setup row 3
        self.__charsPerPixelLabel.grid(column=0, row=3, columnspan=5)
        self.__pixelSpacingLabel.grid(column=7, row=3, columnspan=5)

        # setup row 4
        self.__charsPerPixel.grid(column=0, row=4, columnspan=5)
        self.__pixelSpacing.grid(column=7, row=4, columnspan=5)

        # setup row 5
        self.__colorSettingsLabel.grid(column=0, row=5, columnspan=5)
        self.__hashKeyLabel.grid(column=7, row=5, columnspan=5)

        # setup row 6
        self.__colorSettings.grid(column=0, row=6, columnspan=5)
        self.__hashKey.grid(column=7, row=6, columnspan=5)

    def validate_number(self, val: str) -> bool:
        if val == "" or val is None:
            return True

        try:
            float(val)
            return True
        except:
            return False