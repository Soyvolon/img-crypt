# Last Edit: 2022-10-28
# Author(s): Bounds

from abc import ABC, abstractmethod
from typing import Tuple
from ..Data import SettingsProfile

class ImageModificationServiceInterface(ABC):
    @abstractmethod
    def hide_text_in_image(self, profile: SettingsProfile, text: str, 
        inputPath: str, outputPath: str) -> None:
        """
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
        """
        raise NotImplementedError()

    @abstractmethod
    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "") \
        -> Tuple[SettingsProfile, str]:
        """
        Packs all UI objects for proper display in the application.

        Precondition:
            Image with text hidden inside is provided

        Args:
            string inputPath, string encryptKey = ""

        Output:
            SettingsProfile profile, string text
            
        Postcondition:
            Text and settings profile used to hide text are returned
        """
        raise NotImplementedError()

    @abstractmethod
    def is_encrypted(self, inputPath: str) -> bool:
        """Checks an image to see if it has encrypted text.

        Precondition:
            The input path is an image path.

        Args:
            inputPath (str): The path to the image to check.

        Returns:
            bool: True if the image file has encrypted text.

        Postcondition:
            The image is unmodified but the file handle is closed.
        """
        raise NotImplementedError()
