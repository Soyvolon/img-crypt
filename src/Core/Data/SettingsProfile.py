# Last Edit: 2022-10-28
# Author(s): Bounds, Hayden

from typing import List, Tuple
from uuid import UUID
from .UserProfile import UserProfile

class SettingsProfile():
    COLOR_STANDARD = 0
    COLOR_UNIQUE = 1

    def __init__(self, name: str, charPerPixel: int, pixelSpacing: int, colorSettings: int, encryptKey: str):
        # DB Properties
        self.uuid: UUID = None
        self.userProfile: UserProfile = None

        # Properties
        self.name = name
        self.charPerPixel = charPerPixel
        self.pixelSpacing = pixelSpacing
        self.colorSettings = colorSettings
        self.encryptKey = encryptKey

    def get_header(self) -> List[int]:
        # set a true flag if there is an encrypt key ...
        if (self.encryptKey and not self.encryptKey.isspace()):
            hasEncrypt = 1 # True
        else:
            hasEncrypt = 0 # False
        # ... then return the header as a set of integers.
        return [self.charPerPixel, 
            self.pixelSpacing, 
            self.colorSettings, 
            hasEncrypt]

    @staticmethod
    def build_settings(headerPixels: List[Tuple[int, int, int]], encryptKey: str = None):
        raise NotImplementedError()