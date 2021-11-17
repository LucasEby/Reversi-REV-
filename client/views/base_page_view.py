from abc import ABC, abstractmethod


class BasePageView(ABC):
    def __init__(self) -> None:
        """
        Abstract page view for all others to build off of
        """
        # self.display()

    @abstractmethod
    def display(self) -> None:
        pass
