from server.database_management.database_manager import DatabaseManager

if __name__ == "__main__":
    print("Server running...")

    # Create thread for running database manager
    database_manager: DatabaseManager = DatabaseManager()