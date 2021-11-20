from __future__ import annotations
import socket
import json
import threading
from _thread import start_new_thread
from typing import List, Dict, Any, Tuple, Optional

from server.client_comms.response_manager import ResponseManager

"""
--- Message Formats ---

CLIENT MESSAGES
Check password for login attempt:
    'protocol_type': 'client_login',
    'user_id': user_id,
    'password': password
Create a new user account:
    'protocol_type': 'client_create_account',
    'user': user,
    'password': password
Retrieve an existing user account:
    'protocol_type': 'client_get_account',
    'user_id': user_id
Update the elo in an existing user account:
    'protocol_type': 'client_update_elo',
    'user_id': user_id,
    'elo': elo
Save a currently active game:
    'protocol_type': 'client_save_game',
    'game_id': game_id,
    'user1': user1,
    'user2': user2,
    'p1_first_move': p1_first_move,
    'board': board
Retrieve a saved game:
    'protocol_type': 'client_get_game',
    'game_id': game_id

SERVER MESSAGES
Respond to client login request:
    'protocol_type': 'server_login',
    'login_worked': login_worked
Respond to client create account request:
    'protocol_type': 'server_create_account',
    'create_account_worked': create_account_worked
Respond to client get account request:
    'protocol_type': 'server_get_account',
    'user_id': user_id,         OR     'user_exists': false
    'username': username,
    'preferences': preferences
Respond to client update elo request:
    'protocol_type': 'server_update_elo',
    'elo_update_worked': elo_update_worked
Respond to client request to save a game:
    'protocol_type': 'server_save_game',
    'save_game_worked': save_game_worked
Respond to client request to get a saved game:
    'protocol_type': 'server_get_game',
    'game_id': game_id,         OR     'game_exists': false
    'user1': user1,
    'user2': user2,
    'p1_first_move': p1_first_move,
    'board': board
Respond to an unrecognized client request:
    'protocol_type': 'protocol_breach',
    'unrecognized_protocol_type': client_request_type
"""

HOST = "localhost"
PORT = 7777


class ServerCommsManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Ensure that this class is a Singleton.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ServerCommsManager, cls).__new__(cls)
        return cls._instance

    def run(self) -> None:
        """
        Start the server and listen for client connections and requests. Handle those requests accordingly.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((HOST, PORT))
        except socket.error as e:
            print(e)
            return
        s.listen(2)
        print("Server started, waiting for connections")
        while True:
            try:
                conn, addr = s.accept()
                conn.settimeout(60.0)  # Set timeout to hear from client to 1 minute
                print("Connected to: ", addr)
                start_new_thread(self.__threaded_client, (conn, addr))
            except Exception as e:
                print(e)

    def __send(self, msg: Dict[str, Any], conn: socket.socket, addr: Tuple[int, int]) -> None:
        """
        Send the given dict message to the given client connection.
        """
        # check if the message have specified protocol type and throw ValueError if
        if not msg["protocol_type"]:
            raise ValueError("Message must have a protocol_type.")
        # put '$$' to signify end of message and encapsulate the message
        message: str = json.dumps(msg, ensure_ascii=False) + "$$"
        try:
            conn.sendto(message.encode(), addr)
        except socket.error as e:
            print(e)

    def __threaded_client(self, conn: socket.socket, addr: Tuple[int, int]) -> None:
        """
        Create a client handler within this thread.
        """
        unparsed_messages: str = ""
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    break
                unparsed_messages = self.__parse_data(
                    data, conn, addr, unparsed_messages
                )
            except socket.error:
                break
        print(f"Lost connection to: {addr}")
        conn.close()

    def __parse_data(
        self, data: bytes, conn: socket.socket, addr: Tuple[int, int], unparsed_messages: str
    ) -> str:
        """
        Parse JSON data and then handle it accordingly.
        """
        package: str = data.decode()
        package = unparsed_messages + package
        package: List[str] = package.split("$$")
        # Loop through all messages before last message end symbol
        for p in range(len(package) - 1):
            msg: Dict[str, Any] = json.loads(package[p])
            # Handle response then send response message back to client
            response_msg: Optional[Dict[str, Any]] = ResponseManager().handle_response(msg)
            self.__send(msg=response_msg, conn=conn, addr=addr)
        return package[-1]

    """
    def __handle_data(self, data, conn, addr) -> None:
    """
    # Based on the type of request received, create and send a response.
    """
        # handle client login request
        if data["protocol_type"] == "client_login":
            print("Client requested login check")
            user_id = data["user_id"]
            password = data["password"]
            worked: bool = self.database_manager.check_password(user_id, password)
            response = {"protocol_type": "server_login", "login_worked": str(worked)}
        # handle client create account request
        elif data["protocol_type"] == "client_create_account":
            print("Client requested to create an account")
            user = data["user"]
            password = data["password"]
            worked: bool = self.database_manager.add_account(user, password)
            response = {
                "protocol_type": "server_create_account",
                "create_account_worked": str(worked),
            }
        # handle client get account request
        elif data["protocol_type"] == "client_get_account":
            print("Client requested to get an account")
            user_id = data["user_id"]
            user: Optional[User] = self.database_manager.get_account(user_id)
            if user:
                response = {
                    "protocol_type": "server_get_account",
                    "user_id": str(user_id),
                    "username": str(user.get_username),
                    "preferences": user.get_preference.to_string(),  # TODO add a to_string method in Preferences
                }
            else:
                response = {
                    "protocol_type": "server_get_account",
                    "user_exists": str(False),
                }
        # handle client request to update a user's elo
        elif data["protocol_type"] == "client_update_elo":
            print("Client requested to update an elo")
            user_id = data["user_id"]
            elo = data["elo"]
            worked: bool = self.database_manager.update_elo(user_id, elo)
            response = {
                "protocol_type": "server_update_elo",
                "elo_update_worked": str(worked),
            }
        # handle client request to save a game
        elif data["protocol_type"] == "client_save_game":
            print("Client requested to save a game")
            game_id = data["game_id"]
            user1 = data["user1"]
            user2 = data["user2"]
            p1_first_move = data["p1_first_move"]
            board = data["board"]
            worked: bool = self.database_manager.save_game(
                game_id, user1, user2, p1_first_move, board
            )
            response = {
                "protocol_type": "server_update_elo",
                "save_game_worked": str(worked),
            }
        # handle client request to get a saved game
        elif data["protocol_type"] == "client_get_game":
            print("Client requested to get a saved game")
            game_id = data["game_id"]
            game: Optional[Game] = self.database_manager.get_game(game_id)
            if game:
                response = {
                    "protocol_type": "server_get_game",
                    "game_id": str(game_id),
                    "user1": game.user1.to_string(),  # TODO add a to_string method in class User
                    "user2": game.user2.to_string(),
                    "p1_first_move": str(game.p1_first_move),
                    "board": game.board.to_string(),  # TODO add to_string method in class Board
                }
            else:
                response = {
                    "protocol_type": "server_get_game",
                    "game_exists": str(False),
                }
        else:
            print("Unrecognized request from the client")
            request = data["protocol_type"]
            response = {
                "protocol_type": "protocol_breach",
                "unrecognized_protocol_type": str(request),
            }
        # finally, send the server's response to the client's request
        self.send(response, conn, addr)
    """
