from client.controllers.base_page_controller import BasePageController


class HomeButtonPageController(BasePageController):
    def __init__(self) -> None:
        """
        Specific type of page controller with a home button already handled.
        Many pages could have a home button, so this removes duplicate code.
        """
        super().__init__()
        self._task_execute_dict["home_button"] = self.__execute_task_home_button

    def __handle_home_button(self) -> None:
        self.queue(task_name="home_button")

    def __execute_task_home_button(self) -> None:
        pass
