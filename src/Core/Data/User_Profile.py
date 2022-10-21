import random
class UserProfile():
    def __init__(self, name):
        self.uuid = random.randint(1, 9999)
        self.name = name
        self.settingsProfiles = []