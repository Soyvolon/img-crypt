import tkinter.ttk as ttk
import tkinter as tk
from .Subsections import *
from Core.Services import *

class ImageCryptApp(tk.Tk):
    # REGION CORE
    def __init__(self):
        # call the ttk UI init
        super().__init__()

        # build the service collection
        self.__serviceCollection = {
            # create some instances of these services.
            ImageModificationServiceInterface: ImageModificationService(),
            ProfileManagementServiceInterface: ProfileManagementService(),
            ImageCryptApp: self
        }

        # build the UI
        self.__gen_ui()

        # initialize any additional services.
        frame: AppFrameInterface = self.__serviceCollection[UserSettingsFrame]
        frame.initialize()

        frame = self.__serviceCollection[UserInputFrame]
        frame.initialize()

        frame = self.__serviceCollection[ImagePreviewFrame]
        frame.initialize()

    #END REGION

    # REGION UI GENERATION
    def __gen_ui(self):
        # TODO: Main window size, color, bg, and default texts/colors.
        # this area should be used to set the entire layout without any
        # specific elements. Namely, should create the boundaries for UI-01,
        # UI-02, and UI-03, but not their contents.

        # set the title
        self.wm_title("Image Crypt")
        self.wm_minsize(250, 250)

        # create the overall container
        self.__parentContainer = tk.PanedWindow(
            master=self,
            orient=tk.HORIZONTAL,
            sashrelief=tk.GROOVE,
            sashpad=3
        )

        # create the left and right divisions
        # create the container for UI-02 and UI-03
        self.__userActionFrame = tk.PanedWindow(
            master=self.__parentContainer,
            height=500,
            width=500,
            orient=tk.VERTICAL,
            sashrelief=tk.GROOVE,
            sashpad=3
        )

        self.__serviceCollection[ImagePreviewFrame] = ImagePreviewFrame(self.__parentContainer, self.__serviceCollection)
        self.__serviceCollection[UserInputFrame] = UserInputFrame(self.__userActionFrame, self.__serviceCollection)
        self.__serviceCollection[UserSettingsFrame] = UserSettingsFrame(self.__userActionFrame, self.__serviceCollection)

        # create UI-01
        self.__imagePreviewFrame = self.__serviceCollection[ImagePreviewFrame]

        # create the top and bottom divisions for the
        # input and settings portions

        # create UI-02
        self.__userInputFrame = self.__serviceCollection[UserInputFrame]

        # create UI-03
        self.__userSettingsFrame = self.__serviceCollection[UserSettingsFrame]

        # pack the UI into a displayed state.
        self.__pack_ui()

    def __pack_ui(self):
        self.__parentContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.__userActionFrame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.__imagePreviewFrame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.__imagePreviewFrame.pack_ui()

        self.__userInputFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.__userInputFrame.pack_ui()

        self.__userSettingsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.__userSettingsFrame.pack_ui()

        # configure the paned windows
        # save the user input/settings to the user action frame
        self.__userActionFrame.add(self.__userInputFrame)
        self.__userActionFrame.add(self.__userSettingsFrame)

        # adjust the sash so the text input area is larger than
        # the settings area
        self.__userActionFrame.sash_place(0, 0, 300)

        # add the user control panes
        self.__parentContainer.add(self.__userActionFrame)
        self.__parentContainer.add(self.__imagePreviewFrame)
            
    # END REGION
