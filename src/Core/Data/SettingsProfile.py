from uuid import UUID
from .UserProfile import UserProfile

class SettingsProfile():
    def __init__(self, name: str, charPerPixel: int, pixelSpacing: int, colorSettings: str, encryptKey: str):
        # DB Properties
        self.uuid: UUID = None
        self.userProfile: UserProfile = None

        # Properties
        self.name = name
        self.charPerPixel = charPerPixel
        self.pixelSpacing = pixelSpacing
        self.colorSettings = colorSettings
        self.encryptKey = encryptKey
