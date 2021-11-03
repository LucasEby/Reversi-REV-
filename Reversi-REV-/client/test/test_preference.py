from client.model.user import User
from client.controllers.manage_preferences_page_controller import ManagePreferencesPageController

user: User = User(21, "John")
controller: ManagePreferencesPageController = ManagePreferencesPageController(user)
controller.pref_go()
