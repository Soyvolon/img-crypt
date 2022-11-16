# Last Edit: 2022-10-28
# Author(s): Bounds

from PIL import Image
from cryptography.fernet import Fernet

from typing import List, Tuple
from .ImageModificationServiceInterface import ImageModificationServiceInterface as IMSI
from ..Data import SettingsProfile
from ..Error import ImageProcessingError

class ImageModificationService(IMSI):
    def __init__(self):
        pass

    # TODO Gif support via pillow
    def hide_text_in_image(self, settings: SettingsProfile, text: str, inputPath: str, outputPath: str) -> bool:
        # lets do some input validation
        if not settings:
            raise ValueError(settings)
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
            unique_colors = settings.colorSettings == SettingsProfile.COLOR_UNIQUE

            # ... get the size of the image ...
            w, h = source.size
            # ... and if it is animated ...
            if source.is_animated:
                # ... get the frame count ...
                frames = source.n_frames
            else:
                frames = 1

            # ... then the header values for the image ...
            header = settings.get_header()

            # ... then find the max pixels we are allowed to use for
            # hiding text ...
            max_pixels = (w * h * frames) - len(header)

            # ... if we are using unique colors ...
            if unique_colors:
                old_max = max_pixels
                max_pixels = 0

                try:
                    for fi in range(frames):
                        source.seek(fi)

                        # ... then find the count of all colors in the image ...
                        color_obj = source.getcolors(maxcolors=250000)
                        
                        colors = len(color_obj)
                        # ... and set the max available pixels to the number of colors ...
                        max_pixels += colors
                except:
                    max_pixels = old_max

            # ... if there is some encryption we want to do ....
            if settings.is_encrypted():
                # ... then create the encrypter ...
                fernet = Fernet(settings.encryptKey)
                # ... and encrypt the text ...
                text_actual = fernet.encrypt(text)
            else:
                # ... otherwise do nothing ...
                text_actual = text

            text_actual += 'eof'

            # ... then find out how many pixels we need, by taking the size of the
            # input text, dividing it by the pixels used for each character,
            # then multiplying it by how many unmodified pixels are between each data pixel ...
            pixels_needed = len(text_actual) / settings.charPerPixel * settings.pixelSpacing

            # ... and if the pixels needed is more than the max pixels ...
            if (pixels_needed > max_pixels):
                # ... raise an error with a human readable message ...
                raise ImageProcessingError("The pixels needed for this modification is more than the max available pixels.\n\
                    Make Characters Per Pixel larger, Pixel Spacing smaller, and/or input less text.")

            # ... and then build an array of the text values ...
            text_values = [ord(x) for x in text_actual]

            # ... then define the pixel counter used to differentiate
            # between header and actual pixel values ...
            pixel_count = 0
            # ... the skip counter for skipping pixels ...
            skip_counter = settings.pixelSpacing
            # ... the text iterator ...
            text_iter = iter(text_values)
            # ... and our breakout boolean ...
            out_of_text = False

            # ... for each frame of the image ...
            for findex in range(frames):
                # ... if we are out of text, break out of the loop ...
                if out_of_text:
                    break
                
                # ... move the file to the proper frame ...
                source.seek(findex)

                # ... before we go through the pixels,
                # lets initialize the color dict for if its needed ...
                color_dict = {}

                # ... then, get the images pixels ...
                pixels = source.getdata()
                modded_pixels = []
                for p in pixels:
                # ... if we are out of text, and not using unique colors
                # break out of the loop ...
                    if out_of_text and not unique_colors:
                        break

                    # ... first, get the pixel ...
                    pixel = p
                    def update_pixel(pixel: Tuple, placeDict) -> Tuple:
                        update = []
                        for i in range(len(pixel)):
                            if i in placeDict:
                                update.append(placeDict[i])
                            else:
                                update.append(pixel[i])

                        return tuple(update)

                    # ... determine if this is a header value or not ...
                    if pixel_count < len(header):
                        # ... if it is the header, generate the 
                        # new value ...
                        val = self.__modify_int(pixel[2], 0, header[pixel_count])
                        # ... then assign it to the pixel ...
                        pixel = update_pixel(pixel, {2: val})
                        # ... then up the pixel counter ...
                        pixel_count += 1
                    else:
                        saveNew = True
                        # ... and if we are color matching ...
                        if unique_colors:
                            # ... then check the color dict for the current pixel ...
                            if pixel in color_dict:
                                # ... if it is there, the apply the saved color ...
                                pixelKey = pixel
                                pixel = color_dict[pixel]
                                # ... and don't save a new color ...
                                saveNew = False

                        # ... if we have a skip, then skip this pixel.
                        # In that regard, we always start with the skip ...
                        if skip_counter > 1:
                            # ... drop the counter by 1 ...
                            skip_counter -= 1
                            # ... and go to the next iteration ...
                            continue

                        # ... if we are supposed to save, then ...
                        if saveNew and not out_of_text:
                            # ... for each char in the pixel ...
                            for charNum in range(settings.charPerPixel):
                                # ... get the raw char value ...
                                charRaw: int = next(text_iter, -1)
                                # ... and if its less than 0 (fail code) ...
                                if charRaw < 0:
                                    # ... then tell the pixel loop to quit ...
                                    out_of_text = True
                                    # ... if we aren't running unique colors,
                                    # then break out of the loop ...
                                    if not unique_colors:
                                        break
                                else:
                                    # ... otherwise, get the three digit int
                                    # string ...
                                    charString = '{0:0=3d}'.format(charRaw)
                                    # ... and break that into three separate chars ...
                                    chars = [int(x) for x in charString]

                                    if settings.charPerPixel == 1:
                                        # ... then get modified r,g,b values for the pixel ...
                                        r = self.__modify_int(pixel[0], 0, chars[0])
                                        g = self.__modify_int(pixel[1], 0, chars[1])
                                        b = self.__modify_int(pixel[2], 0, chars[2])

                                        # TODO fix this wonky logic and how the pixels are computed.
                                        if r > 255:
                                            r -= 10
                                        if g > 255:
                                            g -= 10
                                        if b > 255:
                                            b -= 10

                                        # ... then update the pixel with new r,g,b values ...
                                        pixel = update_pixel(pixel, {
                                            0: r,
                                            1: g,
                                            2: b
                                        })

                                    elif settings.charPerPixel == 2:
                                        if charNum == 0:
                                            r = self.__modify_int(pixel[0], 1, chars[0])
                                            r = self.__modify_int(r, 0, chars[1])
                                            g = self.__modify_int(pixel[1], 1, chars[2])

                                            if r > 255:
                                                r -= 100
                                            if g > 255:
                                                g -= 100

                                            pixel = update_pixel(pixel, {
                                                0: r,
                                                1: g
                                            })
                                        else:
                                            g = self.__modify_int(pixel[1], 0, chars[0])
                                            b = self.__modify_int(pixel[2], 1, chars[1])
                                            b = self.__modify_int(b, 0, chars[2])

                                            if g > 255:
                                                g -= 100
                                            if b > 255:
                                                b -= 100

                                            pixel = update_pixel(pixel, {
                                                1: g,
                                                2: b
                                            })

                                    elif settings.charPerPixel == 3:
                                        pixel = update_pixel(pixel, {
                                            charNum: charRaw
                                        })

                                    # ... then, if there is a new color saved ...
                                    if unique_colors:
                                        # ... save it to the dict ...
                                        color_dict[pixelKey] = pixel

                                    skip_counter = settings.pixelSpacing

                    # ... finally, save the pixel ...
                    modded_pixels.append(pixel)

                # ... once we have modified all our pixels,
                # lets update our image ...
                source.putdata(modded_pixels)

            # ... then save the image ...
            source.save(outputPath)

            # ... and finally, if there is leftover text,
            # return false.
            return next(text_iter, None) == None
        
    def reveal_text_in_image(self, inputPath: str, encryptKey: str = "", imageSettings: SettingsProfile = None) -> Tuple[SettingsProfile, str]:
        # Reveal Process:
        #   get header (imageSettings) if it is None
        #   read all pixel data as per the imageSettings
        #   find last sequence of [ord(x) for x in 'eof'] and remove everything after it
        #   convert data to chars
        #   decrypt if needed
        #   return text and settings profile

        # To start, save the settings profile ...
        settings = imageSettings
        if not settings:
            # ... or get one if the profile is not provided ...
            settings = self.get_header(inputPath)

        # ... and if the profile is still None ...
        if not settings:
            # ... then raise an error ...
            raise ImageProcessingError("The provided inputPath does not contain a valid Image Crypt header.")

        # ... next, create the ord list ...
        text_ords = []
        # ... and open the image ...
        with Image.open(inputPath) as source:
            # ... then define a method to pull the place value of a number ...
            def pull_digit(num: int, place: int):
                parts = [x for x in reversed(str(num))]
                return int(parts[place])

            # ... state if we are using unique colors or not ...
            unique_colors = settings.colorSettings == SettingsProfile.COLOR_UNIQUE

            # ... get all the pixels ...
            pixels = source.getdata()
            # ... get the header ...
            header = settings.get_header()
            # ... set our starting pixel count ...
            pixel_count = 0
            # ... the color dict ...
            colors = {}
            # ... and the skip counter ...
            skip_counter = settings.pixelSpacing
            # ... then for each pixel ...
            for pixel in pixels:
                # ... if its in the header, skip it ...
                if pixel_count < len(header):
                    pixel_count += 1
                    continue

                # ... otherwise if we have a skip, then skip this pixel.
                # In that regard, we always start with the skip ...
                if skip_counter > 1:
                    # ... drop the counter by 1 ...
                    skip_counter -= 1
                    # ... and go to the next iteration ...
                    continue

                # ... if no skips, start crunching the numbers ...
                for charNum in range(settings.charPerPixel):
                    # ... if its an already used unique color ...
                    if unique_colors:
                        # ... then just skip this pixel ...
                        if pixel in colors:
                           continue 

                    num = 0
                    if settings.charPerPixel == 1:
                        # ... otherwise pull the r, g, b parts of our ord value
                        hundreds = pull_digit(pixel[0], charNum)
                        tens = pull_digit(pixel[1], charNum)
                        ones = pull_digit(pixel[2], charNum)

                        # ... combine the three into an actual number ...
                        num = self.__build_int_from_list([ones, tens, hundreds])
                    
                    elif settings.charPerPixel == 2:
                        if charNum == 0:
                            hundreds = pull_digit(pixel[0], 1)
                            tens = pull_digit(pixel[0], 0)
                            ones = pull_digit(pixel[1], 1)
                        else:
                            hundreds = pull_digit(pixel[1], 0)
                            tens = pull_digit(pixel[2], 1)
                            ones = pull_digit(pixel[2], 0)

                        # ... combine the three into an actual number ...
                        num = self.__build_int_from_list([ones, tens, hundreds])

                    elif settings.charPerPixel == 3:
                        num = pixel[charNum]

                    # ... then append that number to the ord list ...
                    text_ords.append(num)

                    # ... and if its a unique color, save the pixel ...
                    if unique_colors:
                        colors[pixel] = num

                    # ... and reset the skip if needed ...
                    skip_counter = settings.pixelSpacing
        
        # ... now lets find the eof marker ...
        eof = [ord(x) for x in 'eof']
        # ... and set the needed hit count ...
        needed_hits = len(eof) - 1
        # ... and the starting hit count ...
        start_hits = needed_hits
        # ... the note the last index ...
        last_index = len(text_ords) - 1
        # ... from the last value to the first ...
        for i in range(len(text_ords) - 1, -1, -1):
            # ... if the ord value matches the eof sequence ...
            if text_ords[i] == eof[needed_hits]:
                # ... drop the sequence number ...
                needed_hits -= 1
                # ... and if our sequence is lower than 0 - i.e. complete ...
                if needed_hits < 0:
                    # ... save our new last index ...
                    last_index = i
                    # ... then break out of the loop ...
                    break
            else:
                # ... otherwise, set the needed hits to the eof length ...
                needed_hits = start_hits
        
        # ... once we have our index, get all the text up to that point ...
        valid_text = text_ords[:last_index]
        # ... then turn it into a string ...
        text_string = ""
        for c in [chr(x) for x in valid_text]:
            text_string += c

        # ... then define our final string ...
        final_text = text_string
        # ... and if it is encrypted ...
        if settings.is_encrypted():
            # ... save the encrypt key to the settings profile ...
            settings.encryptKey = encryptKey
            # ... then create the encrypter ...
            fernet = Fernet(settings.encryptKey)
            # ... and encrypt the text ...
            final_text = fernet.encrypt(text_string)

        # ... finally, return the settings and final text.
        return (settings, final_text)

    def get_header(self, inputPath: str) -> SettingsProfile:
        # Create the pixel list ...
        pixels = []
        # ... then open the image ...
        with Image.open(inputPath) as source:
            # ... and for the length of the header ...
            for i in range(SettingsProfile.HEAD_LENGTH):
                try:
                    # ... get the pixel data from the image ...
                    pix = source.getpixel((i, 0))
                    # ... then take only the first three colors and save them
                    # to the pixels list ...
                    pixels.append(tuple(pix[i] for i in range(len(pix)) if i < 3))
                except:
                    # ... if we get here, something went wrong,
                    # and this image does not have a header ...
                    return None

        # ... then build the settings profile from the pixels
        # and return the result.
        return SettingsProfile.build_settings(pixels)

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

        return self.__build_int_from_list(value)

    def __build_int_from_list(self, values):
        new_value = values[0]
        for i in range(1, len(values)):
            new_value += values[i] * (10 ** i)

        return new_value
        