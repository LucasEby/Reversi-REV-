from threading import Thread

from client.controllers.page_machine import PageMachine

if __name__ == "__main__":
    print("Client running...")

    # Create page machine running in its own thread
    page_machine: PageMachine = PageMachine()
    controller_thread: Thread = Thread(target=page_machine.run)
    controller_thread.start()
