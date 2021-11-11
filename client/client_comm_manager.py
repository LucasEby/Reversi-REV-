from typing import Callable
import json
import traceback
from threading import Thread
import socket


ADDRESS = ('127.0.0.1', 7777)


class ClientCommManager:
    # def __init__(self, callback: Callable[[], None]) -> None:
    def __init__(self, receive_key: str) -> None:
        """
        Construct a
        """
        self.receive_key = receive_key
        self.client = socket.socket()
        self.client.connect(ADDRESS)

    def send(self, message: dict) -> None:
        # pkg = self.receive_key + "\n" + message
        # self.client.send(pkg.encode(encoding='utf8'))
        json_msg = json.dumps(message, ensure_ascii=False) + '$$'
        self.client.send(json_msg.encode())

    def handle_receive(self) -> None:
        pcg = self.client.recv(4096)
        if len(pcg) == 0:
            self.client.close()
            # TODO:deal with connection lost
            traceback.print_exc()
            return
        # parse and deal with the data
        self.__parse_data(pcg)
        # ORIGINAL codes
        # received_msg: str = self.client.recv(1024).decode(encoding='utf8')
        # parsed_msg: [str] = received_msg.split("\n")
        # for msg in parsed_msg:
        #     print(msg)

    def __parse_data(self, pcg):
        protocols = pcg.decode()
        protocols = protocols.split('$$')
        # deal with all the protocols except the empty one at last
        for str_protocol in protocols[:-1]:
            protocol = json.loads(str_protocol)
            self.__deal_with_data(protocol)

    def __deal_with_data(self, protocol: dict):
        if protocol['protocol_type'] == 'client_login':
            # 'server_login' gives back result
            print("Client received login feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_match_request':
            # 'server_match_request' gives back the matching opponent
            print("Client received match_request feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_move':
            # 'server_move' gives opponent's move
            print("Client received move feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_elo':
            # 'server_elo' gives back elo
            print("Client received elo feedback:")
            for key, value in protocol.items():
                print(key, value)

    def send_login(self, user_id: int, password: str):
        """
        Login information
        TODO: needs to be put into other file
        """
        data = {
            'protocol_type': 'client_login',
            'user_id': user_id,
            'password': password
        }
        self.send(data)

    def send_game_match_request(self, user_id: int):
        """
        Send a online matching game request
        TODO: needs to be put into other file
        """
        data = {
            'protocol_type': 'client_match_request',
            'user_id': user_id
        }
        self.send(data)

    def send_move(self, player: str):
        """
        Player's move
        TODO: needs to be put into other file
        """
        data = {
            'protocol_type': 'client_move',
            'player': player    # for testing
            # 'x': player.next_move_x,
            # 'y': player.next_move_y
        }
        self.send(data)

    def send_get_elo(self, user_id: int):
        """
        Get elo request
        TODO: needs to be put into other file
        """
        data = {
            'protocol_type': 'client_elo',
            'user_id': user_id
        }
        self.send(data)


if __name__ == '__main__':
    comm = ClientCommManager("key")
    comm.send_get_elo(777)
    comm.send_move("player1")
    comm.send_login(7, "this_is_password~123")
    comm.send_game_match_request(777)
    comm.handle_receive()
