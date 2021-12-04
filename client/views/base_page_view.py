from abc import ABC, abstractmethod
import tkinter as tk

from client.tkinter_gui import TkinterGUI


class BasePageView(ABC):
    def __init__(self) -> None:
        """
        Abstract page view for all others to build off of
        """
        self._frame = tk.Frame(TkinterGUI().get_window())
        self._frame.lift()
        self._frame.pack()

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        for widgets in self._frame.winfo_children():
            widgets.destroy()
        self._frame.destroy()
