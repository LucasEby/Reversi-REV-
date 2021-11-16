import json
from _thread import start_new_thread
from typing import Dict
from socket import error
import socket


protocol_map: Dict[str, str] = {
    "client_login": "server_login",
    "client_create_account": "server_create_account",
    "client_get_account": "server_get_account",
    "client_update_elo": "server_update_elo",
    "client_save_game": "server_save_game",
    "client_get_game": "server_get_game",
}


def test_run_fake_server() -> None:
    """
    The test method imitates a server that listens for clients and puts them onto different threads.
    """
    # Run a server to listen for a connection and then close it
    server_sock = socket.socket()
    server_sock.bind(("127.0.0.1", 7777))
    server_sock.listen()
    print("Waiting for a connection, server started")
    while True:
        client, info = server_sock.accept()
        print("Connected to:", info)
        start_new_thread(threaded_client, (client,))


def threaded_client(client):
    """
    Handles each client by printing out received messages from the client
    :param client: the client connection created
    """
    while True:
        try:
            data: str = client.recv(2048).decode()
            messages: [str] = data.split("$$")

            if not data:
                print("Disconnected")
                break
            else:
                # deal with all the protocols except the empty one at last
                for str_protocol in messages[:-1]:
                    protocol: Dict[str, str] = json.loads(str_protocol)
                    key: str
                    value: str
                    for key, value in protocol.items():
                        print(key, value)
                    protocol_type: str = protocol["protocol_type"]
                    protocol["protocol_type"] = protocol_map[protocol_type]
                    server_protocol: str = (
                        json.dumps(protocol, ensure_ascii=False) + "$$"
                    )
                    client.sendall(server_protocol.encode())
        except error as e:
            print(e)
            break
    print("Lost connection")
    client.close()


if __name__ == "__main__":
    test_run_fake_server()


"""SOME ARCHIVES BELOW"""


def send_game_match_request(user_id: int):
    """
    Send a online matching game request
    TODO: needs to be put into other file
    """
    data = {"protocol_type": "client_match_request", "user_id": user_id}
    # comm.send(data)


def send_move(player: str):
    """
    Player's move
    TODO: needs to be put into other file
    """
    data = {
        "protocol_type": "client_move",
        "player": player  # for testing
        # 'x': player.next_move_x,
        # 'y': player.next_move_y
    }
    # comm.send(data)


def send_get_elo(user_id: int):
    """
    Get elo request
    TODO: needs to be put into other file
    """
    data = {"protocol_type": "client_elo", "user_id": user_id}
    # comm.send(data)
