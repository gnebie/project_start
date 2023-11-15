
import os
import logging
from config.logger import set_logger
from dataclasses import dataclass
import json
from typing import List
from config.parseargs import parser

logger = logging.getLogger(__name__)


@dataclass
class Settings:
    def __init__(self):
        args = parser.parse_args()
        self.args
        self.retrieve_files_data(self.get_config_file_list(args))
        self.retrieve_env_data()
        self.retrieve_parsed_data(args)

    def retrieve_parsed_setings(self, args):
        self.log_folder = args.log_folder
        self.log_file = args.log_file
        self.log_level = args.log_level
        # retrieve the settings here
        pass

    def retrieve_env_setings(self) -> None:
        # retrieve the settings here
        pass 

    def retrieve_files_setings(self, files):
        # retrieve the settings here
        if isinstance(files) == str:
            files = [files]
        for file in files:
            with open(file) as config_file:
                data = json.load(config_file)
                self.retrieve_file_data(data)

    def retrieve_file_data(self, file_data):
        # retrieve the settings here
        pass

    def get_config_file_list(args) -> List[str]:
        return ["config-files/config.json"]


