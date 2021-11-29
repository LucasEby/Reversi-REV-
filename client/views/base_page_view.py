from abc import ABC, abstractmethod
import tkinter as tk


class BasePageView(ABC):
    def __init__(self, window, title="") -> None:
        """
        Abstract page view for all others to build off of
        """
        self.__build_frame(window, title)

    def __build_frame(self, window, title) -> None:
        self._frame = tk.Frame(window, padx=10, pady=10)  # padding=10)
        window.title(title)
        window.resizable(True, True)  # False, False)
        self._frame.pack()

    def _exit(self):
        self._frame.destroy()
        self._frame.quit()

    @abstractmethod
    def display(self) -> None:
        pass
