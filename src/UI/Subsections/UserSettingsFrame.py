# Last Edit: 2022-11-04
# Author(s): Bounds, Hayden

import os
import tkinter.ttk as ttk
import tkinter as tk

from .AppFrameInterface import AppFrameInterface

from Core.Data import *
from Core.Services import *

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

        # create the objects for profile management
        self.__selectedUserProfile = None
        self.__selectedSettingsProfile = None
        self.__userProfileList = []
        self.__settingsProfileList = []
        self.__defaultSettingsProfile = None
        self.__defaultUserProfile = None
        self.__userProfileNames = []
        self.__settingsProfileNames = []

        self._build()

    def initialize(self) -> None:
        # get the services we need
        from Core.Services import ProfileManagementServiceInterface as PMSI

        self.__profileService: PMSI = self.__services[PMSI]

        # initialize the settings profile objects to defaults.
        # this method will also reload the settings
        # profiles for the selected user profile
        self.__refresh_user_profiles()

        self.__initialized = True  
        # we dont need the whole service collection
        self.__services = None    

    def _error_if_not_initialized(self) -> None:
        if not self.__initialized:
            raise Exception("Frame Not Initialized")  

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
            master=self.__userProfileFrame,
            # postcommand=self.__refresh_user_profiles
        )
        self.__userProfile.bind("<<ComboboxSelected>>", self.__user_profile_changed)

        # user profile add button
        self.__addUserProfile = ttk.Button(
            master=self.__userProfileFrame,
            image=self.__addImage,
            command=self.__new_user_profile_pressed
        )

        # user profile delete button
        self.__deleteUserProfile = ttk.Button(
            master=self.__userProfileFrame,
            image=self.__deleteImage,
            command=self.__delete_user_profile_pressed
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
        defaultSP = self.__get_default_settings_profile()
        self.__colorSettings.bind("<<ComboboxSelected>>", self.__user_profile_changed)
        self.__colorSettings.current(defaultSP.colorSettings)
        
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
        self.__charsPerPixel.current(defaultSP.charPerPixel - 1)
        self.__charsPerPixel.bind("<<ComboboxSelected>>", self.__user_profile_changed)

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
            master=self.__settingsProfileFrame,
            # postcommand=self.__refresh_user_profiles
        )
        self.__settingsProfile.bind("<<ComboboxSelected>>", self.__settings_profile_changed)

        # settings profile add button
        self.__addSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__addImage,
            command = self.__new_settings_profile_pressed
        )

        # settings profile delete button
        self.__deleteSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__deleteImage,
            command = self.__delete_settings_profile_pressed
        )

        # settings profile save button
        self.__saveSettingsProfile = ttk.Button(
            master=self.__settingsProfileFrame,
            image=self.__saveImage,
            command=self.__save_settings_profile_pressed
        )

        # pixel spacing label
        self.__pixelSpacingLabel = ttk.Label(
            master=self.__rightFrame,
            text="Pixel Spacing"
        )

        vcmd = (self.register(self.validate_number), '%P')

        # pixel spacing input
        self.__pixelSpacing = ttk.Combobox(
            master=self.__rightFrame,
            values=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        )
        self.__pixelSpacing.current(defaultSP.pixelSpacing)
        self.__pixelSpacing.bind("<<ComboboxSelected>>", self.__user_profile_changed)

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
        self.__hashKey.insert(0, self.__defaultSettingsProfile.encryptKey)

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

    # REGION Profiles
    def __user_profile_changed(self, *args):
        self._error_if_not_initialized()
        selectedProfileName = self.__userProfile.get()
        for item in self.__userProfileList:
            if item.name[0][0] == selectedProfileName:
                self.__selectedUserProfile = item
        self.__refresh_user_profiles()

    def __new_user_profile_pressed(self):
        self._error_if_not_initialized()
        name = tk.simpledialog.askstring("Name of User Profile", "Enter the name of the User Profile")
        if name != None:
            self.__selectedUserProfile = self.__profileService.create_user_profile(name)

    def __delete_user_profile_pressed(self):
        self._error_if_not_initialized()
        self.__profileService.delete_user_profile(self.__selectedUserProfile.key)
        self.__refresh_user_profiles

    def __settings_profile_changed(self, *args):
        self._error_if_not_initialized()
        selectedProfileName = self.__settingsProfile.get()
        for item in self.__settingsProfileList:
            if item.name[0][0] == selectedProfileName:
                self.__selectedSettingsProfile = item
        self.__refresh_user_profiles()

    def __new_settings_profile_pressed(self):
        self._error_if_not_initialized()
        self.__user_profile_changed()
        name = tk.simpledialog.askstring("Name of Settings Profile", "Enter the name of the Settings Profile")
        if name != None:
            self.__selectedSettingsProfile = self.__profileService.create_settings_profile(name, self.__selectedUserProfile.key)

    def __delete_settings_profile_pressed(self):
        self._error_if_not_initialized()
        self.__profileService.delete_settings_profile(self.__selectedSettingsProfile.key)
        self.__refresh_settings_profiles

    def __save_settings_profile_pressed(self):
        self._error_if_not_initialized()
        self.__selectedSettingsProfile.charPerPixel = self.__charsPerPixel.get()
        self.__selectedSettingsProfile.pixelSpacing = self.__pixelSpacing.get()
        self.__selectedSettingsProfile.colorSettings = self.__colorSettings.current()
        self.__selectedSettingsProfile.encryptKey = self.__hashKey.get()
        if self.__hashKey.get() == "":
            self.__selectedSettingsProfile.encryptKey = None
        self.__profileService.update_settings_profile(self.__selectedSettingsProfile, self.__selectedUserProfile.key[0])
    
    # END REGION

    # REGION Settings
    def __chars_per_pixel_changed(self):
        self._error_if_not_initialized()
        pass

    def __color_settings_changed(self):
        self._error_if_not_initialized()
        pass

    def __pixel_spacing_changed(self):
        self._error_if_not_initialized()
        pass

    def __hash_key_changed(self):
        self._error_if_not_initialized()
        pass

    # END REGION

    # REGION Public Methods
    def get_current_settings(self) -> SettingsProfile:
        """Returns the currently loaded settings profile.

        Precondition:
            This frame is initialized.

        Args:
            None

        Returns:
            SettingsProfile: The currently loaded settings profile.

        Postcondition:
            The settings profile object is returned.
        """
        self._error_if_not_initialized()
        return self.__selectedSettingsProfile \
            if self.__selectedSettingsProfile \
            else self.__defaultSettingsProfile
    def get_temp_profile(self, tempProfile: SettingsProfile) -> None:
        """Fetches a temporary profile that will be pulled from an image header

        Precondition:
            This frame is initialized.

        Args:
            The temporary profile
        
        Returns:
            None

        Postcondition:
            The temp profile is retrieved and  differentiated from more permanent profiles
        """
        self._error_if_not_initialized()
        pass
    # END REGION

    # REGION Private Methods
    def __refresh_user_profiles(self) -> None:
        """Loads all user profiles from the database and
        resets the user profile list to contain only these
        profiles and the default one.
        """
        default = self.__get_default_user_profile()
        # TODO load profiles from database
        # TODO add rest of profiles from db
        self.__userProfileList = [default] 
        self.__userProfileList = self.__profileService.get_all_user_profiles()
        self.__userProfileNames = []
        for item in self.__userProfileList:
            self.__userProfileNames.append(item.name[0][0])
        '''if not self.__selectedUserProfile in self.__userProfileList:
            self.__selectedUserProfile = self.__defaultUserProfile'''

        # TODO reload dropdown data
        self.__userProfile['values'] = self.__userProfileNames

        self.__refresh_settings_profiles()

    def __refresh_settings_profiles(self) -> None:
        """Loads all settings profiles from the database for the
        currently loaded user profiles and resets the settings profile 
        list to contain only these profiles and the default one.
        """
        default = self.__get_default_settings_profile()
        # TODO load profiles from database. Needs to be specific to the currently selected
        # user profile
        # TODO add rest of profiles from db
        self.__settingsProfileNames.clear()
        self.__settingsProfileList = [default]
        if self.__selectedUserProfile != None:
            self.__profileService.get_settings_profiles_for_user(self.__selectedUserProfile)
            self.__settingsProfileList = self.__selectedUserProfile.settingsProfiles
            for item in self.__selectedUserProfile.settingsProfiles:
                if item not in self.__settingsProfileNames:
                    self.__settingsProfileNames.append(item.name)
            '''
        if not self.__selectedSettingsProfile in self.__settingsProfileList:
            self.__selectedSettingsProfile = self.__defaultSettingsProfile
            '''
            # TODO update input fields
            print(self.__settingsProfileNames)
        self.__selectedSettingsProfile = self.__get_default_settings_profile()
        self.__pixelSpacing["text"] = self.__selectedSettingsProfile.pixelSpacing
        self.__hashKey["text"] = self.__selectedSettingsProfile.encryptKey
        self.__settingsProfile['values'] = self.__settingsProfileNames
        # TODO reload dropdown data

    def __get_default_user_profile(self) -> UserProfile:
        """Gets the default user profile object and binds the
        default settings profile object to it.

        Returns:
            UserProfile: The default user profile object.
        """
        if not self.__defaultUserProfile:
            self.__defaultUserProfile = UserProfile('<default>')
            settings = self.__get_default_settings_profile()
            self.__defaultUserProfile.settingsProfiles.append(settings)
            settings.userProfile = self.__defaultUserProfile

        return self.__defaultUserProfile

    def __get_default_settings_profile(self) -> SettingsProfile:
        """Gets the default settings profile object.

        Returns:
            SettingsProfile: The default settings profile object.
        """
        if not self.__defaultSettingsProfile:
            self.__defaultSettingsProfile = SettingsProfile(
                name='<default>',
                charPerPixel=1,
                pixelSpacing=1,
                colorSettings=SettingsProfile.COLOR_STANDARD,
                encryptKey=''
            )

        return self.__defaultSettingsProfile

    # END REGION
