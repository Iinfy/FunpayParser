import json
import os
from logger import log
import config as cfg


def check_config_exists():
    return os.path.exists("config.json")

def import_settings():
    with open("config.json") as config:
        cfg.parser_settings = json.load(config)
    log.debug(f"Settings loaded: {cfg.parser_settings}")


def export_settings():
    with open("config.json", "w") as config:
        json.dump(cfg.parser_settings, config, indent=4)

def reset_default_settings():
    settings = {
        "parsing_mode" : 2,
        "parsing_frequency" : 15
    }
    with open("config.json", "w") as config:
        json.dump(settings, config, indent=4)