import random
class SettingsProfile():
    def __init__(self, name, charPerPixel, pixelSpacing, colorSettings, encryptKey, userProfile):
        self.uuid = random.randint(1, 9999)
        self.name = name
        self.charPerPixel = charPerPixel
        self.pixelSpacing = pixelSpacing
        self.colorSettings = colorSettings
        self.encryptKey = encryptKey
        self.userProfile = userProfile