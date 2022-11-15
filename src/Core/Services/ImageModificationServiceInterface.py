# Last Edit: 2022-10-28
# Author(s): Bounds

from abc import ABC, abstractmethod
from typing import Tuple
from ..Data import SettingsProfile

class ImageModificationServiceInterface(ABC):
    @abstractmethod
    def hide_text_in_image(self, profile: SettingsProfile, text: str, 
        inputPath: str, outputPath: str) -> bool:
        """
        Hides text within given image with using settings corresponding to the settings profile
        
        Precondition:
            Image attached must be of valid format
            
        Args:
            SettingsProfile profile, string text, string inputPath, string 
            outputPath
        
        Output:
            (bool): True if all text has been hidden into the image.
        
        Postcondition:
            Image with hidden text is saved to the location matching inputPath
        """
        raise NotImplementedError()

    @abstractmethod
    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "",
        imageSettings: SettingsProfile = None) -> Tuple[SettingsProfile, str]:
        """
        Packs all UI objects for proper display in the application.

        Precondition:
            Image with text hidden inside is provided

        Args:
            inputPath (str): The path to the image to open.
            encryptKey (str): The key to decrypt the text data.
            imageSettings (SettingsProfile): A settings profile. Leave null
            to gather a settings profile from the image.

        Output:
            SettingsProfile profile, string text
            
        Postcondition:
            Text and settings profile used to hide text are returned
        """
        raise NotImplementedError()

    @abstractmethod
    def get_header(self, inputPath: str) -> SettingsProfile:
        """Returns the header for an image at the provided path if
        a header is present.

        Precondition:
            An image is present at inputPath

        Args:
            inputPath (str): The path to check.

        Returns:
            SettingsProfile: A settings profile if a header was
            detected. None if no header is present.

        Postcondition:
            The image is unmodified but the file handle is closed.
        """
        raise NotImplementedError()
