from abc import ABC, abstractmethod
import tkinter as tk


class BasePageView(ABC):
    def __init__(self) -> None:
        """
        Abstract page view for all others to build off of
        """
        # self.display()
        self._window = tk.Tk()

    @abstractmethod
    def display(self) -> None:
        pass
