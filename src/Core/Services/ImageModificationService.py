# Last Edit: 2022-10-28
# Author(s): Bounds

from typing import Tuple
from .ImageModificationServiceInterface import ImageModificationServiceInterface as IMSI
from ..Data import SettingsProfile

class ImageModificationService(IMSI):
    def __init__(self):
        pass

    def hide_text_in_image(self, profile: SettingsProfile, text: str, inputPath: str, outputPath: str) -> None:
        return super().hide_text_in_image(profile, text, inputPath, outputPath)

    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "") -> Tuple[SettingsProfile, str]:
        return super().reveal_text_in_image(inputPath, encryptKey)

    def is_encrypted(self, inputPath: str) -> bool:
        return super().is_encrypted(inputPath)