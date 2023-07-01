import json
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    feeds_path: str
    target_route_ids: List[str]


def load_config():
    with open("./config.json") as config_file:
        config_dict = json.loads(config_file.read())
    return Config(
        feeds_path=config_dict["feedsPath"],
        target_route_ids=config_dict["targetRouteIds"],
    )
