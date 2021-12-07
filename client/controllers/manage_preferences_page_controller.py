from typing import Callable
from client.model.abstract_rule import AbstractRule
from client.views.manage_preferences_page_view import ManagePreferencesPageView
from client.model.preference import Preference
from client.model.user import User
from client.controllers.home_button_page_controller import HomeButtonPageController


class ManagePreferencesPageController(HomeButtonPageController):
    """
    This class represents a controller for Manage Preferences Page. It outputs to the view for Manage Preferences Page.
    It also takes input and make changes to the user's preference setting accordingly.
    """

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        preferences_complete_callback: Callable[[], None],
        back_to_pick_game_callback: Callable[[User], None],
        user: User,
    ) -> None:
        """
        Construct the controller with a view for the passed in user

        :param go_home_callback: Callback for when user wants to go to home page
        :param preferences_complete_callback: Callback for when preferences have been updated
        :param user: The user who is interacting with Manage Preferences Page
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict["change_preferences"] = self.execute_change_preferences

        # Old values:
        # I figure we can just store them initially and just rewrite all values to simplify the code
        self._preference: Preference = user.get_preference()
        self._board_size: int = user.get_preference().get_board_size()
        self._board_color: str = user.get_preference().get_board_color()
        self._main_user_disk_color: str = user.get_preference().get_my_disk_color()
        self._opponent_disk_color: str = user.get_preference().get_opp_disk_color()
        self._chosen_rule: AbstractRule = user.get_preference().get_rule()
        self._end_home_callback: Callable[[], None] = preferences_complete_callback
        self._back_to_pick_game_callback: Callable[
            [User], None
        ] = back_to_pick_game_callback

        self._user: User = user
        self._view: ManagePreferencesPageView = ManagePreferencesPageView(
            go_home_callback=go_home_callback,
            user=user,
            set_preferences_cb=self.execute_change_preferences,
        )

    def execute_change_preferences(self, preference: Preference):
        self.queue(task_name="change_preferences", task_info=preference)
        self._view.destroy()
        self._back_to_pick_game_callback(self._user)
