# Last Edit: 2022-10-28
# Author(s): Bounds, Hayden

class UserProfile():
    def __init__(self, name: str):
        # DB Properties
        self.key: int = None
        self.settingsProfiles = []

        # Properties
        self.name = name
