from abc import ABC  # , abstractmethod
import tkinter as tk


class BasePageView(ABC):
    def __init__(self, window, title="") -> None:
        """
        Abstract page view for all others to build off of
        """
        self.__build_frame(window, title)

    def __build_frame(self, window, title) -> None:
        self._frame = tk.Frame(window, padding=10)
        self._frame.tk.title(title)
        # Make it so the window is not resizable
        self._frame.tk.resizable(False, False)
