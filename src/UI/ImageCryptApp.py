import tkinter as tk
from wsgiref import validate
from Subsections import ImagePreviewFrame as ipf

class ImageCryptApp(tk.Tk):
    # REGION CORE
    def __init__(self):
        # call the TK UI init
        super().__init__()

        # TODO: initialize services


        # build the UI
        self.__gen_ui()
    #END REGION

    # REGION UI GENERATION
    # NOTE: UI generation execution should be done in the
    # order of the UI generation methods in this region.

    def __gen_ui(self):
        self.__gen_main_window()
        self.__gen_image_preview()
        self.__gen_user_input()
        self.__gen_user_settings()

    def __gen_main_window(self):
        # TODO: Main window size, color, bg, and default texts/colors.
        # this area should be used to set the entire layout without any
        # specific elements. Namely, should create the boundaries for UI-01,
        # UI-02, and UI-03, but not their contents.

        # set the title
        self.title = "Image Crypt"

        # create the left and right divisions
        # create the container for UI-02 and UI-03
        self.__userActionFrame = tk.Frame(
                master=self,
                relief=tk.RAISED,
                borderwidth=1, 
                height=500
            )
        self.__userActionFrame.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT, expand=True)

        # create UI-01
        self.__imagePreviewFrame = ipf.ImagePreviewFrame()
        self.__imagePreviewFrame.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT, expand=True)

        # create the top and bottom divisions for the
        # input and settings portions

        # create UI-02
        self.__userInputFrame = tk.Frame(
                master=self.__userActionFrame,
                #bg="blue", 
                width=600
            )
        self.__userInputFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        # create UI-03
        self.__userSettingsFrame = tk.Frame(
                master=self.__userActionFrame,
                #background="red"
            )
        self.__userSettingsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def __gen_image_preview(self):
        # TODO: The image preview section. Should contain UI-01.
        pass

    def __gen_user_input(self):
        # TOOD: The user input section. Should contain UI elements
        # within UI-02.

        # the frame for the user input controls
        frame = self.__userInputFrame



        pass

    def __gen_user_settings(self):
        # TODO: The user settings section. Should contain UI elements
        # within UI-03
        pass
    # END REGION

    # REGION INPUT VALIDATION
    # TODO: Build input validation code for the UI.
    # END REGION

    # REGION CONTROL CODE
    # TODO: Handle button presses. by passing calls with the proper values to the various services
    # and displaying those results correctly.
    # END REGION




