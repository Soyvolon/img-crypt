# Last Edit: 2022-10-28
# Author(s): Bounds

from PIL import Image
import numpy

from typing import List, Tuple
from .ImageModificationServiceInterface import ImageModificationServiceInterface as IMSI
from ..Data import SettingsProfile
from ..Error import ImageProcessingError

class ImageModificationService(IMSI):
    def __init__(self):
        pass

    # use source.putdata() to put the data back in the image.
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

            # ... then the header values for the image ...
            header = profile.get_header()

            # ... then find the max pixels we are allowed to use for
            # hiding text ...
            max_pixels = (w * h) - len(header)
            # ... then find out how many pixels we need, by taking the size of the
            # input text, dividing it by the pixels used for each character,
            # then multiplying it by how many unmodified pixels are between each data pixel ...
            pixels_needed = len(text) / profile.charPerPixel * profile.pixelSpacing

            # ... and if the pixels needed is more than the max pixels ...
            if (pixels_needed > max_pixels):
                # ... raise an error with a human readable message ...
                raise ImageProcessingError("The pixels needed for this modification is more than the max available pixels.\n\
                    Make Characters Per Pixel larger, Pixel Spacing smaller, and/or input less text.")

            # ... otherwise, get the images pixels ...
            pixels = list(source.getdata())
            # ... then the image mode ...
            if source.mode == "RGBA":
                channels = 4
            elif source.mode == "RGB":
                channels = 3
                    
            # ... then get a numpy array of the pixel values ...
            # pixel_values = numpy.array(pixels).reshape((h, w, channels))

            # ... and an array of the text values ...
            text_values = [ord(x) for x in text]

            # ... before we go through the pixels,
            # lets initialize the color dict if needed ...
            if profile.colorSettings == SettingsProfile.COLOR_UNIQUE:
                color_dict = {}

            # ... then define the pixel counter used to differentiate
            # between header and actual pixel values ...
            pixel_count = 0
            for pindex in range(len(pixels)):
                # ... first, get the pixel ...
                pixel = pixels[pindex]
                def assign_to_pixel(place: int, val: int):
                    pixel = tuple([pixel[i] if i != place else val for i in range(len(pixel))])

                # ... determine if this is a header value or not ...
                if pixel_count < len(header):
                    # ... if it is the header, generate the 
                    # new value ...
                    val = self.__modify_int(pixel[2], 0, header[pixel_count])
                    # ... then assign it to the pixel ...
                    assign_to_pixel(2, val)
                    # ... then up the pixel counter ...
                    pixel_count += 1
                else:
                    # ... otherwise, compute the pixel data ...
                    pass

                # ... finally, save the pixel
                pixels[pindex] = pixel
        

    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "") -> Tuple[SettingsProfile, str]:
        return super().reveal_text_in_image(inputPath, encryptKey)

    def is_encrypted(self, inputPath: str) -> bool:
        return super().is_encrypted(inputPath)

    def __modify_int(self, start: int, place: int, new: int) -> int:
        """Modifies a digit in an integer

        Args:
            start (int): The value to modify
            place (int): The place value to modify, where 0 is the 1s place and -1 is the last digit.
            new (int): The new value to insert into the value. Should be a value (0-9).

        Returns:
            int: The new integer
        """
        value = [int(x) for x in reversed(str(start))]
        # ... then set the value ...
        value[place] = new
        # ... then assign the value back to an integer ...

        if len(value) <= 0:
            return 0

        new_value = value[0]
        for i in range(1, len(value)):
            new_value += value[i] * (10 ** i)

        return new_value
        