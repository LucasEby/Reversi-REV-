from server.server_comms_manager import ServerCommsManager

if __name__ == "__main__":
    print("Server running...")
    server = ServerCommsManager()
    server.run()
