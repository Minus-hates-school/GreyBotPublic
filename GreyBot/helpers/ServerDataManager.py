import discord
from discord.ui import View,Select

class ServerConfigManager:
    def __init__(self,manager):
        super().__init__()
        self.manager = manager

        self.add_item(
            Select(
                placeholder="Selecting setting",
                options=[
                    discord.SelectOption(label="Prefix",value="prefix"),
                    discord.SelectOption(label="Enable Welcome",value="welcome_enabled"),
                ],
                custom_id="config_menu"
            )
        )

    def AdminMenu(self):
        self.add_item(
            Select(
                placeholder="Selecting setting",
                options=[
                    discord.SelectOption(label="Prefix", value="prefix"),
                    discord.SelectOption(label="Enable Welcome", value="welcome_enabled"),
                ],
                custom_id="config_menu"
            )
        )

