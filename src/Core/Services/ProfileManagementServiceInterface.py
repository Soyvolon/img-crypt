# Last Edit: 2022-10-28
# Author(s): Bounds

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..Data import *

class ProfileManagementServiceInterface(ABC):
    @abstractmethod
    def create_user_profile(self, name: str) -> UserProfile:
        """Creates a new user profile.

        Precondition:
            None

        Args:
            name (str): The name of the new user profile.

        Returns:
            UserProfile: The created user profile object.

        Postcondition:
            A new user profile with a matching name is saved
            in the local database.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_user_profile(self, key: UUID) -> bool:
        """Deletes a user profile.

        Precondition:
            The profile with the provided key exists

        Args:
            key (UUID): The key of the profile to delete.

        Returns:
            bool: True if the operation completed successfully.

        Postcondition:
            The user profile matching the key is no longer
            saved in the dictionary nor in memory.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_user_profiles(self) -> List[UserProfile]:
        """Get all existing user profiles.

        Precondition:
            None

        Args:
            None

        Returns:
            List[UserProfile]: The list of user profiles.

        Postcondition:
            None
        """
        raise NotImplementedError()

    @abstractmethod
    def get_settings_profiles_for_user(self, profile: UserProfile) -> None:
        """Updates the provided profile object with it's settings
        profiles from the database.

        Precondition:
            The user profile has a UUID key and is present
            in the database.

        Args:
            profile (UserProfile): The user profile to update.

        Postcondition:
            The user profile object has all it's settings profiles
            propagated from the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_settings_profile(self, name: str, parentKey: UUID) -> SettingsProfile:
        """Create a new settings profile.

        Precondition:
            The provided parent key exists in the database.

        Args:
            name (str): The name of the new settings profile.
            parentKey (UUID): The key of the parent user profile.

        Returns:
            SettingsProfile: The settings profile object.

        Postcondition:
            A new settings profile is present in the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_settings_profile(self, key: UUID) -> bool:
        """Delete an existing settings profile.

        Precondition:
            The provided key is present in the database.

        Args:
            key (UUID): The key of the settings profile to delete.

        Returns:
            bool: True if this operation completed successfully.

        Postcondition:
            The present key no longer exists in the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_settings_profiles(self) -> List[SettingsProfile]:
        """Get all existing settings profiles.

        Precondition:
            None

        Args:
            None

        Returns:
            List[SettingsProfile]: The list of settings profiles.

        Postcondition:
            None
        """
        raise NotImplementedError()

    @abstractmethod
    def get_settings_profile(self, key: UUID) -> SettingsProfile:
        """Get a specific settings profile.

        Precondition:
            The provided key exists in the database.

        Args:
            key (UUID): The key of the settings profile to get.

        Returns:
            SettingsProfile: The fully populated settings profile object.

        Postcondition:
            The returned object data matches the database data.
        """
        raise NotImplementedError()

    @abstractmethod
    def update_settings_profile(updatedProfile: SettingsProfile) -> bool:
        """Update an existing settings profile.

        Precondition:
            The key in the settings profile object
            exists in the database

        Args:
            updatedProfile (SettingsProfile): The settings profile 
            to update the database with

        Returns:
            bool: True if this operation is successful.

        Postcondition:
            The database is updated to match the values
            in the updatedProfile object.
        """
        raise NotImplementedError()