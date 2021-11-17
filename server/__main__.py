from server.server_comms_manager import ServerCommsManager
from _thread import start_new_thread

if __name__ == "__main__":
    server = ServerCommsManager()
    start_new_thread(server.run(), ())
