import os
from typing import Dict, Any, Optional, NamedTuple

from yaml import load, Loader


class ServerInfo(NamedTuple):
    server_ip: str
    server_port: int


class ConfigReader:
    _FILE = "server_config.yaml"
    _singleton = None

    def __init__(self):
        self._server_info: Optional[ServerInfo] = None
        self._parse_yaml()

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(ConfigReader, cls).__new__(cls)
        return cls._singleton

    def get_server_info(self) -> Optional[ServerInfo]:
        """
        Gets the server information
        :return: server info if found, None if configuration not found
        """
        return self._server_info

    def _parse_yaml(self) -> None:
        """
        Parses the configuration YAML from the expected format into ConfigReader fields
        """

        # Try reading file
        data_dict: Dict[Any]
        file_stream = None
        try:
            file_path: str = os.path.join(os.path.dirname(__file__), self._FILE)
            file_stream = open(file_path)
            data_dict = load(file_stream, Loader=Loader)
        except Exception:
            return
        finally:
            if file_stream is not None:
                file_stream.close()

        # Extract data from dictionary into private fields
        if "server" in data_dict:
            server_file_info: Dict[Any] = data_dict["server"]
            if "server_ip" in server_file_info and "server_port" in server_file_info:
                self._server_info = ServerInfo(
                    server_ip=server_file_info["server_ip"],
                    server_port=server_file_info["server_port"],
                )
