from server.client_comms.response_manager import ResponseManager
from server.client_comms.server_comms_manager import ServerCommsManager
from _thread import start_new_thread

from server.database_management.database_manager import DatabaseManager

if __name__ == "__main__":
    server: ServerCommsManager = ServerCommsManager()
    start_new_thread(server.run, ())

    response_manager: ResponseManager = ResponseManager()
    start_new_thread(response_manager.run, ())

    database_manager: DatabaseManager = DatabaseManager()
    start_new_thread(database_manager.run, ())

    # Pause forever
    while True:
        pass
