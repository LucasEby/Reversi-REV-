import os
from typing import Dict, Any, Optional, NamedTuple

from yaml import load, Loader


class DatabaseAccessInfo(NamedTuple):
    host_ip: str
    username: str
    password: str


class ConfigReader:

    _FILE = "server_config.yaml"
    _singleton = None

    def __init__(self):
        self._database_access_info: Optional[DatabaseAccessInfo] = None
        self._parse_yaml()

    @classmethod
    def get_instance(cls):
        if cls._singleton is None:
            cls._singleton = ConfigReader()
        return cls._singleton

    def get_database_access_info(self) -> Optional[DatabaseAccessInfo]:
        """
        Gets the database information
        :return: Database info if found, None if configuration not found
        """
        return self._database_access_info

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
        if "database" in data_dict:
            database_info: Dict[Any] = data_dict["database"]
            if (
                "host_ip" in database_info
                and "username" in database_info
                and "password" in database_info
            ):
                self._database_access_info = DatabaseAccessInfo(
                    host_ip=database_info["host_ip"],
                    username=database_info["username"],
                    password=database_info["password"],
                )
