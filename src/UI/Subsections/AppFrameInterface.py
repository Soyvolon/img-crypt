# Last Edit: 2022-10-28
# Author(s): Bounds

from abc import ABC, abstractmethod
import tkinter.ttk as ttk

class AppFrameInterface(ABC, ttk.Labelframe):
    @abstractmethod
    def _error_if_not_initialized(self) -> None:
        """Raises an error if the class is not initialized.

        Raises:
            Error: The error for not being initialized. 
        """
        raise NotImplementedError()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

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
        raise NotImplementedError()
    
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
        raise NotImplementedError()