from queue import Queue
from typing import Dict, Callable, Any, Union


class BasePageController:
    def __init__(self) -> None:
        """
        PageController containing functions and attributes that all page controllers should have.
        Contains internals for queueing tasks and executing them, making interface to other page
        controllers as simple as possible.
        """
        self._queue: Queue = Queue()
        self._task_execute_dict: Dict[
            str, Union[Callable[[Any], None], Callable[[], None]]
        ] = {}

    def run(self) -> None:
        """
        Waits for task to be queued then executes that task
        """
        next_task: str
        next_task_info: Any
        # Get task from queue
        next_task, next_task_info = self._queue.get()
        # Execute task if known
        if next_task in self._task_execute_dict:
            if next_task_info is None:
                self._task_execute_dict[next_task]()
            else:
                self._task_execute_dict[next_task](next_task_info)

    def queue(self, task_name: str, task_info: Any = None) -> None:
        """
        Queue tasks in the correct format so child classes don't need to know that format

        :param task_name: Name of the task
        :param task_info: Additional info associated with the task, as 1 data type
        """
        self._queue.put((task_name, task_info))
