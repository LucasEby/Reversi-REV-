from threading import Thread

from client.controllers.page_controller_machine import PageControllerMachine

if __name__ == "__main__":
    print("Client running...")

    # Create page machine running in its own thread
    page_machine: PageControllerMachine = PageControllerMachine()
    controller_thread: Thread = Thread(target=page_machine.run)
    controller_thread.start()
