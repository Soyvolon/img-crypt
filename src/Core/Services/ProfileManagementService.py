# Last Edit: 2022-10-28
# Author(s): Bounds

from typing import List
from uuid import UUID
from .ProfileManagementServiceInterface import ProfileManagementServiceInterface as PMSI
from ..Data import *

class ProfileManagementService(PMSI):
    def __init__(self):
        # TODO database conn work here.
        pass

    # -- User Profiles --
    def create_user_profile(self, name: str) -> UserProfile:
        return super().create_user_profile(name)

    def delete_user_profile(self, key: UUID) -> bool:
        return super().delete_user_profile(key)

    def get_all_user_profiles(self) -> List[UserProfile]:
        return super().get_all_user_profiles()

    def get_settings_profiles_for_user(self, profile: UserProfile) -> None:
        return super().get_settings_profiles_for_user(profile)

    # -- -- --
    # -- Settings Profiles --
    def create_settings_profile(self, name: str, parentKey: UUID) -> SettingsProfile:
        return super().create_settings_profile(name, parentKey)

    def delete_settings_profile(self, key: UUID) -> bool:
        return super().delete_settings_profile(key)

    def update_settings_profile(updatedProfile: SettingsProfile) -> bool:
        return super().update_settings_profile()

    def get_all_settings_profiles(self) -> List[SettingsProfile]:
        return super().get_all_settings_profiles()

    def get_settings_profile(self, key: UUID) -> SettingsProfile:
        return super().get_settings_profile(key)

    # -- -- --