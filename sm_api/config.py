from pathlib import Path

import ujson


class Config:
    def __init__(self, conf_path: str):
        self.conf_path = conf_path
        self.required_fields = ["database", "jwt_secret", "logging"]

    @staticmethod
    def __conf_exists(conf_path: str) -> bool:
        file_path = Path(conf_path)

        if file_path.exists():
            return True

        return False

    @staticmethod
    def __conf_data(conf_path: str) -> dict:
        with open(conf_path) as f:
            return ujson.loads(f.read())

    def __conf_required_keys(self, conf_data: dict) -> str or None:
        provided_keys = conf_data.keys()

        for required_key in self.required_fields:
            if required_key not in provided_keys:
                return required_key

    def __conf_redundant_keys(self, conf_data: dict) -> str or None:
        provided_keys = conf_data.keys()

        for provided_key in provided_keys:
            if provided_key not in self.required_fields:
                return provided_key

    def read(self):
        assert self.__conf_exists(self.conf_path), "Configuration file does not exists: {}".format(self.conf_path)

        data = self.__conf_data(self.conf_path)

        required_key = self.__conf_required_keys(data)

        assert required_key is None, "This section is required, but not provided: {}".format(required_key)

        redundant_key = self.__conf_redundant_keys(data)
        assert redundant_key is None, "This section is redundant and should not be used: {}".format(redundant_key)

        return data
