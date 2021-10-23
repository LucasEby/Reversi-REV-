from client.controllers.page_machine import PageMachine

if __name__ == "__main__":
    print("Client running...")
    page_machine: PageMachine = PageMachine()
    page_machine.run()
