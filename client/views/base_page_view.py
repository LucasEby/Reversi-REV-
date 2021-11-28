from abc import ABC  # , abstractmethod
import tkinter as tk


class BasePageView(ABC):
    def __init__(self, window, title="") -> None:
        """
        Abstract page view for all others to build off of
        """
        self.__build_frame(window, title)
<<<<<<< Updated upstream
=======
        # self.display()
>>>>>>> Stashed changes

    def __build_frame(self, window, title) -> None:
        self._frame = tk.Frame(window)  # , padx=10, pady=10)  # padding=10)
        window.title(title)
        window.resizable(True, True)  # False, False)
        # self._frame.tk.title(title)
        # Make it so the window is not resizable
<<<<<<< Updated upstream
        self._frame.tk.resizable(False, False)
=======
        # self._frame.tk.resizable(False, False)
        self._frame.pack()

    @abstractmethod
    def display(self) -> None:
        pass
>>>>>>> Stashed changes
