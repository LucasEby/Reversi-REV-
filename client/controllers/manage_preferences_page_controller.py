import time
from typing import Callable

from client.model.account import Account
from client.server_comms.save_preferences_server_request import (
    SavePreferencesServerRequest,
)
from client.views.manage_preferences_page_view import ManagePreferencesPageView
from client.model.preference import Preference
from client.model.user import User
from client.controllers.home_button_page_controller import HomeButtonPageController


class ManagePreferencesPageController(HomeButtonPageController):
    """
    This class represents a controller for Manage Preferences Page. It outputs to the view for Manage Preferences Page.
    It also takes input and make changes to the user's preference setting accordingly.
    """

    _UPDATE_PREFERENCES_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        preferences_complete_callback: Callable[[User], None],
        user: User,
    ) -> None:
        """
        Construct the controller with a view for the passed in user

        :param go_home_callback: Callback for when user wants to go to home page
        :param preferences_complete_callback: Callback for when preferences have been updated
        :param user: The user who is interacting with Manage Preferences Page
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict[
            "change_preferences"
        ] = self.__execute_change_preferences

        self._preferences_complete_callback: Callable[
            [User], None
        ] = preferences_complete_callback

        self._user: User = user
        self._view: ManagePreferencesPageView = ManagePreferencesPageView(
            go_home_callback=self.handle_home_button,
            user=user,
            set_preferences_cb=self.__handle_change_preferences,
        )

    def __handle_change_preferences(self, preference: Preference) -> None:
        """
        Handle change to preferences via queue

        :param preference: Preference to change
        """
        self.queue(task_name="change_preferences", task_info=preference)

    def __execute_change_preferences(self, task_info) -> None:
        """
        Change preferences of main user

        :param task_info: Preferences to change
        """
        preference: Preference = task_info
        self._user.set_preference(preference)
        if isinstance(self._user, Account):
            self.__update_preferences_in_database(self._user)
        self._view.destroy()
        self._preferences_complete_callback(self._user)

    def __update_preferences_in_database(self, account: Account) -> None:
        """
        Updates the preferences for this account in the database.

        :param account: the account whose preferences should be updated
        """
        try:
            server_request: SavePreferencesServerRequest = SavePreferencesServerRequest(
                account
            )
            server_request.send()
            start_time: float = time.time()
            while server_request.is_response_success() is None:
                if time.time() - start_time > self._UPDATE_PREFERENCES_TIMEOUT_SEC:
                    raise ConnectionError(
                        "Server unresponsive. Game could not be created"
                    )
            if server_request.is_response_success() is False:
                raise ConnectionError("Server could not properly save preferences")
        except ConnectionError as e:
            # TODO: Notify view of server error
            print(e)
