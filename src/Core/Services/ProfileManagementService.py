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

    def delete_user_profile(self, key: int) -> bool:
        keyTup = (key[0],)
        self.c.execute(''' DELETE FROM UserProfiles WHERE Key=?''', keyTup)

    def get_all_user_profiles(self) -> List[UserProfile]:
        self.c.execute('''SELECT key FROM UserProfiles''')
        name = ''
        userProfileList = []
        for item in self.c.fetchall():
            self.c.execute("""SELECT name FROM UserProfiles WHERE Key=?""", (item[0],))
            name = self.c.fetchall()
            profile = UserProfile(name)
            profile.uuid = item
            userProfileList.append(profile)
        return userProfileList


    def get_settings_profiles_for_user(self, parentKey: int) -> None:
        #Bug here, for some reason there's apparently a value error on the next line
        self.c.execute('''SELECT key FROM SettingsProfiles WHERE UserProfile=?''', (int(parentKey[0])))
        settingsProfileList = []
        name = ''
        charPerPixel = 0
        pixelSpacing = 0
        colorSettings = 0
        encryptKey = ''
        for item in self.c.fetchall():
            self.c.execute("""SELECT Name FROM SettingsProfiles WHERE Key=?""", (item[0],))
            name = self.c.fetchall()
            self.c.execute("""SELECT CharPerPixel FROM SettingsProfiles WHERE Key=?""", (item[0],))
            charPerPixel = self.c.fetchall()
            self.c.execute("""SELECT PixelSpacing FROM SettingsProfiles WHERE Key=?""", (item[0],))
            pixelSpacing = self.c.fetchall()
            self.c.execute("""SELECT ColorSettings FROM SettingsProfiles WHERE Key=?""", (item[0],))
            colorSettings = self.c.fetchall()
            self.c.execute("""SELECT EncryptionKey FROM SettingsProfiles WHERE Key=?""", (item[0],))
            encryptKey = self.c.fetchall()
            profile = SettingsProfile(name, charPerPixel, pixelSpacing, colorSettings, encryptKey)
            profile.uuid = item
            settingsProfileList.append(profile)
        return settingsProfileList

    # -- -- --
    # -- Settings Profiles --
    def create_settings_profile(self, name: str, parentKey: int) -> SettingsProfile:
        newProfile = SettingsProfile(name, 0, 0, 0, "")
        values = (name, '', '', '', None, int(parentKey[0]))
        self.c.execute('''INSERT INTO SettingsProfiles(Name, CharPerPixel, PixelSpacing, ColorSettings, EncryptionKey, UserProfile) VALUES(?,?,?,?,?,?)''', values)
        self.conn.commit()

    def delete_settings_profile(self, key: int) -> bool:
        keyTup = (key[0],)
        self.c.execute(''' DELETE FROM SettingsProfiles WHERE Key=?''', keyTup)

    def update_settings_profile(self, updatedProfile: SettingsProfile) -> bool:
        self.c.execute('''UPDATE SettingsProfiles SET CharPerPixel = ?, PixelSpacing = ?, ColorSettings = ?, EncryptionKey = ? WHERE Key = ?''', (updatedProfile.charPerPixel, updatedProfile.pixelSpacing, updatedProfile.colorSettings, updatedProfile.encryptKey, updatedProfile.uuid))
        self.conn.commit()

    def get_all_settings_profiles(self) -> List[SettingsProfile]:
        self.c.execute('''SELECT key FROM SettingsProfiles''')
        settingsProfileList = []
        name = ''
        charPerPixel = 0
        pixelSpacing = 0
        colorSettings = 0
        encryptKey = ''
        for item in self.c.fetchall():
            self.c.execute("""SELECT Name FROM SettingsProfiles WHERE Key=?""", (item[0],))
            name = self.c.fetchall()
            self.c.execute("""SELECT CharPerPixel FROM SettingsProfiles WHERE Key=?""", (item[0],))
            charPerPixel = self.c.fetchall()
            self.c.execute("""SELECT PixelSpacing FROM SettingsProfiles WHERE Key=?""", (item[0],))
            pixelSpacing = self.c.fetchall()
            self.c.execute("""SELECT ColorSettings FROM SettingsProfiles WHERE Key=?""", (item[0],))
            colorSettings = self.c.fetchall()
            self.c.execute("""SELECT EncryptionKey FROM SettingsProfiles WHERE Key=?""", (item[0],))
            encryptKey = self.c.fetchall()
            profile = SettingsProfile(name, charPerPixel, pixelSpacing, colorSettings, encryptKey)
            profile.uuid = item
            settingsProfileList.append(profile)
        return settingsProfileList


    def get_settings_profile(self, key: int) -> SettingsProfile:
        self.c.execute("""SELECT * FROM SettingsProfiles WHERE Key = ?""", (key, ))
        return self.c.fetchall()

    # -- -- --
