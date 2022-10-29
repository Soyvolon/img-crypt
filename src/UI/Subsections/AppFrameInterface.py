from abc import ABC, abstractmethod
import tkinter.ttk as ttk

class AppFrameInterface(ABC, ttk.Labelframe):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def _build(self) -> None:
        """
        Creates the child objects for this frame.

        Precondition:
            The parent frame, self, is initialized.

        Args:
            None

        Returns:
            None

        Postcondition:
            The child elements are initialized.
        """
        pass
    
    @abstractmethod
    def pack_ui(self) -> None:
        """
        Packs all UI objects for proper display in the application.

        Precondition:
            All child objects have been created.

        Args:
            None

        Returns:
            None

        Postcondition:
            All child elements are packed into proper UI displays
        """
        pass