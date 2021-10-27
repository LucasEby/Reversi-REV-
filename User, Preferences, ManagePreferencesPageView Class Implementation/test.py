from manage_preferences_page_controller import ManagePreferencesPageController
from manage_preferences_page_view import ManagePreferencesPageView
from user import User


user = User(21, "got7")
controller = ManagePreferencesPageController(user)
controller.pref_go()