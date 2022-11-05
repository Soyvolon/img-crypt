# Last Edit: 2022-11-04
# Author(s): Bounds Hayden

from typing import List
from uuid import UUID
from .ProfileManagementServiceInterface import ProfileManagementServiceInterface as PMSI
from ..Data import *
import sqlite3

class ProfileManagementService(PMSI):
    def __init__(self):
        # TODO database conn work here. This can be handled by a passed variable during init
        # or just a hard coded string. Either way, its going to be a hard coded value - the user
        # wont get a choice in this storage location.
        self.conn = sqlite3.connect(r".\ImgCrpytDB.db")
        self.c = self.conn.cursor()
        #I declared key as int because I wasn't sure what you wanted me to do with UUID generation
        self.c.execute(""" CREATE TABLE IF NOT EXISTS UserProfiles (
        Key INTEGER PRIMARY KEY,
        Name varchar(256) NOT NULL); """)
        self.c.execute(""" CREATE TABLE IF NOT EXISTS SettingsProfiles (
        Key INTEGER PRIMARY KEY,
        Name varchar(256) NOT NULL,
        CharPerPixel int,
        PixelSpacing bigint,
        ColorSettings int,
        EncryptionKey varchar(256),
        UserProfile int NOT NULL); """)

    # -- User Profiles --
    def create_user_profile(self, name: str) -> UserProfile:
        newProfile = UserProfile(name)
        c = self.conn.cursor()
        c.execute(''' INSERT INTO UserProfiles(Name) VALUES (?)''', (name,))
        self.conn.commit()
        newProfile.uuid = c.lastrowid
        print(newProfile.uuid)
        #Unsure what to do with the UUID part of creation
        #When using this method, leave out the key part UUID should autogenerate

    def delete_user_profile(self, key: UUID) -> bool:
        keyTup = (key,)
        self.c.execute(''' DELETE FROM UserProfiles WHERE Key=?''', keyTup)

    def get_all_user_profiles(self) -> List[UserProfile]:
        self.c.execute('''SELECT * FROM UserProfiles''')
        return self.c.fetchall()

    def get_settings_profiles_for_user(self, profile: UserProfile) -> None:
        keyTup = (profile.UUID,)
        self.c.execute('''SELECT * FROM SettingsProfiles WHERE UserProfile=?''', keyTup)

    # -- -- --
    # -- Settings Profiles --
    def create_settings_profile(self, name: str, parentKey: UUID) -> SettingsProfile:
        newProfile = SettingsProfile(name, 0, 0, "", "")
        #Unsure how you want me to deal with UUID generation
        values = ('', name, '', '', '', '', parentKey)
        self.c.execute('''INSERT INTO SettingsProfiles(Key, Name, CharPerPixel, PixelSpacing, ColorSettings, EncryptionKey, UserProfile) VALUES(?,?,?,?,?,?,?)''', values)

    def delete_settings_profile(self, key: UUID) -> bool:
        keyTup = (key,)
        self.c.execute(''' DELETE FROM SettingsProfiles WHERE Key=?''', keyTup)

    def update_settings_profile(updatedProfile: SettingsProfile) -> bool:
        return super().update_settings_profile()

    def get_all_settings_profiles(self) -> List[SettingsProfile]:
        self.c.execute('''SELECT * FROM SettingsProfiles''')
        return self.c.fetchall()

    def get_settings_profile(self, key: UUID) -> SettingsProfile:
        return super().get_settings_profile(key)

    # -- -- --
