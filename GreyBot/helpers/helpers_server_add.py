import os
import discord
import toml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
BASE_PATH = Path(__file__).parent.parent / "Servers"

class Server:
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self.guild_id = str(guild.id)
        self.folder_path = BASE_PATH / self.guild_id
        self.config_path = self.folder_path / "config.toml"
        self.example_path = BASE_PATH / "_EXAMPLE.toml"
        self.config = {}

        logger.info(f"Initializing server: {self.guild.name} ({self.guild_id})")
        self._ensure_folder()
        self._load_or_create_config()

    def _ensure_folder(self):
        if not self.folder_path.exists():
            logger.info(f"Creating folder for guild {self.guild_id}")
            self.folder_path.mkdir(parents=True, exist_ok=True)

    def _load_or_create_config(self):
        if self.config_path.exists():
            logger.info(f"Loading config from {self.config_path}")
            self.config = toml.load(self.config_path)
        else:
            logger.info(f"Creating default config from {self.example_path}")
            self.config = toml.load(self.example_path)
            self.save_config()

    def get_setting(self, key: str):
        return self.config.get("settings", {}).get(key)

    def set_setting(self, key: str, value):
        self.config.setdefault("settings", {})[key] = value
        self.save_config()

    def save_config(self):
        logger.info(f"Saving config to {self.config_path}")
        try:
            with open(self.config_path, "w") as f:
                toml.dump(self.config, f)
        except FileNotFoundError:
            print("yeah thats THE POINT.")

# Optional helper
def init_server(guild: discord.Guild) -> Server:
    return Server(guild)
