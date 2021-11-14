from client.client_comm_manager import ClientCommManager
from client.credential_check_request import CredentialCheckRequest

if __name__ == '__main__':
    """
    The main program to start a client side connection to check the login information.
    """
    comm = ClientCommManager("key", "call")
    # comm.send_get_elo(777)
    # comm.send_move("player1")
    while True:
        username: str = input("Enter your username: ")
        password: str = input("Enter your password: ")
        if username == 'q' or password == 'q':
            comm.close_the_connection()
            exit(0)
        login = CredentialCheckRequest(comm)
        # login.send_login("newPlayer", "this_is_password~123")
        login.send_login(username, password)
        login.check_credential_check_request()
    # comm.send_game_match_request(777)


def send_game_match_request(user_id: int):
    """
    Send a online matching game request
    TODO: needs to be put into other file
    """
    data = {
        'protocol_type': 'client_match_request',
        'user_id': user_id
    }
    comm.send(data)


def send_move(player: str):
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
    comm.send(data)


def send_get_elo(user_id: int):
    """
    Get elo request
    TODO: needs to be put into other file
    """
    data = {
        'protocol_type': 'client_elo',
        'user_id': user_id
    }
    comm.send(data)
