from _thread import start_new_thread
from threading import Thread

from client.controllers.page_machine import PageMachine
from client.server_comms.client_comms_manager import ClientCommsManager

if __name__ == "__main__":
    print("Client running...")

    client_comms_manager: ClientCommsManager = ClientCommsManager()
    start_new_thread(client_comms_manager.run, ())

    # Create page machine running in its own thread. Once it has stopped, program is over
    page_machine: PageMachine = PageMachine()
    #start_new_thread(page_machine.run, ())
    page_machine.run()

