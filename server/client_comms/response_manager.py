from threading import Lock
from typing import Dict, Any

from common.client_server_protocols import (
    create_game_client_schema,
    get_game_client_schema,
    update_elo_client_schema,
    get_top_elos_client_schema,
    save_game_client_schema,
    save_preferences_client_schema,
    create_account_client_schema,
    credential_check_client_schema,
    matchmaker_client_schema,
)
from server.client_comms.base_client_response import BaseClientResponse
from server.client_comms.create_game_client_response import CreateGameClientResponse
from server.client_comms.credential_check_client_response import (
    CredentialCheckClientResponse,
)
from server.client_comms.save_game_client_response import SaveGameClientResponse
from server.client_comms.save_preferences_client_response import (
    SavePreferencesClientResponse,
)
from server.client_comms.get_game_client_response import GetGameClientResponse
from server.client_comms.get_top_elos_client_response import GetTopELOsClientResponse
from server.client_comms.update_elo_client_response import UpdateELOClientResponse
from server.client_comms.create_account_client_response import (
    CreateAccountClientResponse,
)
from server.client_comms.matchmaker_client_response import MatchmakerClientResponse


class ResponseManager:
    _instance = None
    _lock: Lock = Lock()
    _protocol_type_response_dict: Dict[str, str] = {
        create_game_client_schema.schema[
            "protocol_type"
        ]: CreateGameClientResponse.__name__,
        save_game_client_schema.schema[
            "protocol_type"
        ]: SaveGameClientResponse.__name__,
        save_preferences_client_schema.schema[
            "protocol_type"
        ]: SavePreferencesClientResponse.__name__,
        get_game_client_schema.schema["protocol_type"]: GetGameClientResponse.__name__,
        update_elo_client_schema.schema[
            "protocol_type"
        ]: UpdateELOClientResponse.__name__,
        get_top_elos_client_schema.schema[
            "protocol_type"
        ]: GetTopELOsClientResponse.__name__,
        save_game_client_schema.schema[
            "protocol_type"
        ]: SaveGameClientResponse.__name__,
        create_account_client_schema.schema[
            "protocol_type"
        ]: CreateAccountClientResponse.__name__,
        credential_check_client_schema.schema[
            "protocol_type"
        ]: CredentialCheckClientResponse.__name__,
        matchmaker_client_schema.schema[
            "protocol_type"
        ]: MatchmakerClientResponse.__name__,
    }

    def __new__(cls, *args, **kwargs):
        """
        Ensure RequestManager is a singleton
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ResponseManager, cls).__new__(cls)
        return cls._instance

    def handle_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds a response to the queue for future execution based on the protocol type of the given message
        :param message: Message passed from the server comms manager
        """
        # Check prototype type in message is valid
        if "protocol_type" not in message:
            return {}
        if message["protocol_type"] not in self._protocol_type_response_dict:
            return {}
        # Queue response based on protocol type of incoming message
        new_response: BaseClientResponse = globals()[
            self._protocol_type_response_dict[message["protocol_type"]]
        ](message)
        return new_response.respond()
