import tomllib
import toml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

base = Path(__file__).parent
settings = base / "BotSettings.toml"
def load_setting(section,key) -> str:
    logger.info(f"Loading {section} - {key}")
    with open(settings,"rb") as f:
        setting = tomllib.load(f)
    return f"{setting[section][key]}"


def update_setting(section,key,new):
    logger.info(f"Updating {section} - {key} with value: {new}")
    with open(settings,"r") as f:
        setting = toml.load(f)
    setting[section][key] = new
    with open(settings,"w") as f:
        toml.dump(setting,f)

