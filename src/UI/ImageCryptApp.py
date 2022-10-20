import tkinter as ttk
from wsgiref import validate
from UI.Subsections.ImagePreviewFrame import ImagePreviewFrame
from UI.Subsections.UserInputFrame import UserInputFrame
from UI.Subsections.UserSettingsFrame import UserSettingsFrame

class ImageCryptApp(ttk.Tk):
    # REGION CORE
    def __init__(self):
        # call the ttk UI init
        super().__init__()

        # TODO: initialize services


        # build the UI
        self.__gen_ui()
    #END REGION

    # REGION UI GENERATION
    def __gen_ui(self):
        # TODO: Main window size, color, bg, and default texts/colors.
        # this area should be used to set the entire layout without any
        # specific elements. Namely, should create the boundaries for UI-01,
        # UI-02, and UI-03, but not their contents.

        # set the title
        self.title = "Image Crypt"

        # create the overall container
        self.__parentContainer = ttk.PanedWindow(
            master=self,
            orient=ttk.HORIZONTAL,
            sashrelief=ttk.GROOVE,
            sashpad=3
        )

        # create the left and right divisions
        # create the container for UI-02 and UI-03
        self.__userActionFrame = ttk.PanedWindow(
            master=self.__parentContainer,
            height=500,
            orient=ttk.VERTICAL,
            sashrelief=ttk.GROOVE,
            sashpad=3
        )

        # create UI-01
        self.__imagePreviewFrame = ImagePreviewFrame(self.__parentContainer)

        # create the top and bottom divisions for the
        # input and settings portions

        # create UI-02
        self.__userInputFrame = UserInputFrame(self.__userActionFrame)

        # create UI-03
        self.__userSettingsFrame = UserSettingsFrame(self.__userActionFrame)

        # pack the UI into a displayed state.
        self.__pack_ui()

    def __pack_ui(self):
        self.__parentContainer.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)

        self.__userActionFrame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)

        self.__imagePreviewFrame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)
        self.__imagePreviewFrame.pack_ui()

        self.__userInputFrame.pack(fill=ttk.BOTH, side=ttk.TOP, expand=True)
        self.__userInputFrame.pack_ui()

        self.__userSettingsFrame.pack(fill=ttk.BOTH, side=ttk.TOP, expand=True)
        self.__userSettingsFrame.pack_ui()

        # configure the paned windows
        # save the user input/settings to the user action frame
        self.__userActionFrame.add(self.__userInputFrame)
        self.__userActionFrame.add(self.__userSettingsFrame)

        # add the user control panes
        self.__parentContainer.add(self.__userActionFrame)
        self.__parentContainer.add(self.__imagePreviewFrame)
            
    # END REGION
