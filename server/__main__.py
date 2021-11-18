from server.client_comms.response_manager import ResponseManager
from server.client_comms.server_comms_manager import ServerCommsManager
from _thread import start_new_thread

if __name__ == "__main__":
    server = ServerCommsManager()
    start_new_thread(server.run, ())

    response_manager = ResponseManager()
    start_new_thread(response_manager.run, ())
