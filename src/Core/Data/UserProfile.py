from uuid import UUID

class UserProfile():
    def __init__(self, name: str):
        # DB Properties
        self.uuid: UUID = None
        self.settingsProfiles = []

        # Properties
        self.name = name
