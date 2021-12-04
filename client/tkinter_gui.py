from threading import Lock

import tkinter as tk


class TkinterGUI:

    _singleton = None
    _lock: Lock = Lock()
    _window: tk.Tk = tk.Tk()

    def __new__(cls, *args, **kwargs):
        """
        Singleton
        """
        if not cls._singleton:
            with cls._lock:
                if not cls._singleton:
                    cls._singleton = super(TkinterGUI, cls).__new__(cls)
                    cls._singleton.__setup_window()
        return cls._singleton

    def __setup_window(self) -> None:
        """
        Sets up the window with properties
        """
        self._window.title("Reversi")
        self._window.resizable(True, True)

    def get_window(self) -> tk.Tk:
        """
        Gets tkinter window
        :return: Window
        """
        return self._window

    def run(self) -> None:
        """
        Run Tkinter GUI
        """
        self._window.mainloop()
