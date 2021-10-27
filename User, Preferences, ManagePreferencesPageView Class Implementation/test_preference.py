from manage_preferences_page_controller import ManagePreferencesPageController
from user import User


user = User(21, "John")
controller = ManagePreferencesPageController(user)
controller.pref_go()
