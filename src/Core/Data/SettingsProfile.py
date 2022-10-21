class SettingsProfile():
    def __init__(self, name, charPerPixel, pixelSpacing, colorSettings, encryptKey, userProfile):
        self.uuid = 0
        self.name = name
        self.charPerPixel = charPerPixel
        self.pixelSpacing = pixelSpacing
        self.colorSettings = colorSettings
        self.encryptKey = encryptKey
        self.userProfile = userProfile
