import threading
from _thread import start_new_thread
import time
from threading import Thread

from client.model.account import Account
from client.server_comms.cancel_match_server_request import CancelMatchServerRequest
from client.server_comms.client_comms_manager import ClientCommsManager
from client.server_comms.create_account_server_request import CreateAccountServerRequest
from client.server_comms.matchmaker_server_request import MatchmakerServerRequest


if __name__ == "__main__":
    print("Client running...")

    client_comms_manager: ClientCommsManager = ClientCommsManager()
    start_new_thread(client_comms_manager.run, ())

    account: Account = Account("username", 0, None)
    server_request: CreateAccountServerRequest = CreateAccountServerRequest(
        account, "password"
    )
    server_request.send()
    start_time: float = time.time()
    while server_request.is_response_success() is None:
        if time.time() - start_time > 1:  # self._SAVE_GAME_TIMEOUT_SEC:
            raise ConnectionError("Server unresponsive. Game could not be saved")
    if server_request.is_response_success() is False:
        raise ConnectionError("Server could not properly create account")
    ac_id: int = server_request.get_account_id()
    print("account_id: " + str(ac_id))
    account.set_account_id(ac_id)
    server_request_matchmaker: MatchmakerServerRequest = MatchmakerServerRequest(
        account
    )
    # start_new_thread(server_request_matchmaker.send, ())
    server_request_matchmaker.send()
    start_time_matchmaker: float = time.time()
    while server_request_matchmaker.is_response_success() is not False:
        # if time.time() - start_time_matchmaker > 1:  # self._SAVE_GAME_TIMEOUT_SEC:
        #     print(
        #         "Server unresponsive. Possible match not found yet"
        #     )
        if server_request_matchmaker.is_response_success() is True:
            print("game_id: " + str(server_request_matchmaker.get_game_id()))
            print("opp_username: " + str(server_request_matchmaker.get_opp_username()))
            print("opp_elo: " + str(server_request_matchmaker.get_opp_elo()))
            print(
                "get_player_term: " + str(server_request_matchmaker.get_player_term())
            )
            break

        # server_request_cancel_match: CancelMatchServerRequest = CancelMatchServerRequest(
        #     account
        # )
        # # start_new_thread(server_request_cancel_match.send, ())
        # server_request_cancel_match.send()
        # start_time_cancel: float = time.time()
        # if server_request_cancel_match.is_response_success() is None:
        #     if time.time() - start_time_cancel > 1:  # self._SAVE_GAME_TIMEOUT_SEC:
        #         print(
        #             "Server unresponsive. Match not cancelled successfully yet"
        #         )
        # if server_request_cancel_match.is_response_success() is False:
        #     raise ConnectionError("Server could not properly cancel the match")
        # print("success: True")
    if server_request_matchmaker.is_response_success() is False:
        raise ConnectionError("Server could not properly make match")

    # x1 = threading.Thread(target=thread_matchmaking, args=(account,))
    # x1.start()
    # x1.join()
    # x2 = threading.Thread(target=thread_matchmaking, args=(account2,))
    # x2.start()
