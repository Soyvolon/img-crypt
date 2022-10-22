from abc import ABC, abstractmethod

class ServicesInterface(ABC):
    @abstractmethod
    def HideTextInImage(self) -> None:
        '''
        Hides text within given image with using settings corresponding to the settings profile
        
        Precondition:
            Image attached must be of valid format
            
        Args:
            SettingsProfile profile, string text, string inputPath, string 
            outputPath
        
        Output:
            None
        
        Postcondition:
            Image with hidden text is saved to the location matching inputPath
        '''
        pass
    
    def RevealTextInImage(self) -> None:
        '''
        Packs all UI objects for proper display in the application.

        Precondition:
            Image with text hidden inside is provided
        Args:
            string inputPath, string encryptKey = “”
        Output:
            SettingsProfile profile, string text
        Postcondition:
            Text and settings profile used to hide text are returned
        '''
        pass
#Will complete the rest of the docstrings next week
    def IsEncrypted(self) -> None:
        pass

    def GetHeaderValues(self) -> None:
        pass

    def SetHeaderValues(self) -> None:
        pass

    def HideTextInPixel(self) -> None:
        pass

    def GetTextFromPixel(self) -> None:
        pass

    def CreateUserProfile(self) -> None:
        pass

    def DeleteUserProfile(self) -> None:
        pass

    def GetAllUserProfiles(self) -> None:
        pass

    def GetSettingsProfilesForUserProfile(self) -> None:
        pass

    def CreateSettingsProfile(self) -> None:
        pass

    def DeleteSettingsProfile(self) -> None:
        pass

    def GetAllSettingsProfile(self) -> None:
        pass

    def GetSettingsProfile(self) -> None:
        pass

    def UpdateSettingsProfile(self) -> None:
        pass