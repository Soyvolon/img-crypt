# Last Edit: 2022-10-28
# Author(s): Bounds

from PIL import Image
import numpy

from typing import List, Tuple
from .ImageModificationServiceInterface import ImageModificationServiceInterface as IMSI
from ..Data import SettingsProfile

class ImageModificationService(IMSI):
    def __init__(self):
        pass

    def hide_text_in_image(self, profile: SettingsProfile, text: str, inputPath: str, outputPath: str) -> None:
        # lets do some input validation
        if not profile:
            raise ValueError(profile)
        if not text:
            text = ''
        if not inputPath:
            raise ValueError(inputPath)
        if not outputPath:
            raise ValueError(outputPath)

        # lets process some images!
        # ... start by loading the image into
        # memory in a way we can get the pixels ...
        with Image.open(inputPath) as source:
            # ... get the size of the image ...
            w, h = source.size
            # ... and its pixels ...
            pixels = list(source.getdata())
            # ... then the image mode ...
            if source.mode == "RGBA":
                channels = 4
            elif source.mode == "RGB":
                channels = 3
            # ... then get a numpy array of the pixel values ...
            pixel_values = numpy.array(pixels).reshape((h, w, channels))

            


    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "") -> Tuple[SettingsProfile, str]:
        return super().reveal_text_in_image(inputPath, encryptKey)

    def is_encrypted(self, inputPath: str) -> bool:
        return super().is_encrypted(inputPath)
