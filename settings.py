import json
import os
from logger import log

parser_settings = None

def check_config_exists():
    return os.path.exists("config.json")

def import_settings():
    global parser_settings
    with open("config.json") as config:
        parser_settings = json.load(config)
    log.debug(f"Imported settings: {parser_settings}")


def export_settings():
    global parser_settings
    with open("config.json", "w") as config:
        json.dump(parser_settings, config, indent=4)

def reset_default_settings():
    settings = {
        "parsing_mode" : 2,
        "parsing_frequency" : 15,
        "logging_level" : "WARNING"
    }
    with open("config.json", "w") as config:
        json.dump(settings, config, indent=4)