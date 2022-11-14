# Last Edit: 2022-10-28
# Author(s): Bounds, Hayden

from typing import List, Tuple
from .UserProfile import UserProfile

class SettingsProfile():
    COLOR_STANDARD = 0
    COLOR_UNIQUE = 1

    HEAD_LENGTH = 4

    def __init__(self, name: str, charPerPixel: int, pixelSpacing: int, \
        colorSettings: int, encryptKey: str):
        # DB Properties
        self.key: int = None
        self.userProfile: UserProfile = None

        # Properties
        self.name = name
        self.charPerPixel = charPerPixel
        self.pixelSpacing = pixelSpacing
        self.colorSettings = colorSettings
        self.encryptKey = encryptKey
        self.__builtFromPixelsEncryptFlag = False

    def is_encrypted(self) -> bool:
        return self.__builtFromPixelsEncryptFlag or \
            (self.encryptKey and not self.encryptKey.isspace())

    def get_header(self) -> List[int]:
        # set a true flag if there is an encrypt key ...
        if self.is_encrypted():
            hasEncrypt = 1 # True
        else:
            hasEncrypt = 0 # False
        # ... then create the header as a set of integers ...
        header = [self.charPerPixel, 
            self.pixelSpacing, 
            self.colorSettings, 
            hasEncrypt]

        # ... and make sure its the same length as the
        # head length var ...
        assert len(header) == SettingsProfile.HEAD_LENGTH

        # ... finally, return the header.
        return header

    def toggle_build_encrypt_flag(self) -> None:
        self.__builtFromPixelsEncryptFlag = not self.__builtFromPixelsEncryptFlag

    @staticmethod
    def build_settings(headerPixels: List[Tuple[int, int, int]]):
        # ... if the provided list of pixels is not the same
        # length as the head length says it should be ...
        if len(headerPixels) != SettingsProfile.HEAD_LENGTH:
            # ... raise an error ...
            raise ValueError(headerPixels, "Header length does not \
                match provided pixels.")
        
        data = []

        # ... otherwise, for each value in the header ...
        for pixel in headerPixels:
            # ... get the B color ...
            b = pixel[2]
            # ... and get the ones place of it ...
            val = b % 10
            # ... then save that in into the data list ...
            data.append(val)

        # ... next, validate the provided values ...
        # ... if the char per pixel is less than 0
        # or more than 3, return None.
        if data[0] < 0 or data[0] > 3:
            return None

        # ... if the pixel spacing is less than 0
        # return None
        if data[1] < 0:
            return None

        # ... if the color settings is not standard
        # or unique, return None
        if data[2] != SettingsProfile.COLOR_STANDARD and \
            data[2] != SettingsProfile.COLOR_UNIQUE:
            return None

        # ... and if the encrypt flag is not 1 or 0,
        # return None
        if data[3] != 0 and data[3] != 1:
            return None

        # ... then save the data into the proper
        # fields ...
        profile = SettingsProfile(
            '<import>',
            data[0],
            data[1],
            data[2],
            ''
        )

        # ... and if there was encryption ...
        if data[3] == 1:
            # ... set the encrypt flag to True ...
            profile.toggle_build_encrypt_flag()

        # ... then return the new profile.
        return profile