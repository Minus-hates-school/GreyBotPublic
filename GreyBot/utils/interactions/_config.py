from discord.ui import View, Select
import discord

class ConfigMenu(View):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.add_item(
            Select(
                placeholder="Select a setting to update...",
                options=[
                    discord.SelectOption(label="Prefix", value="prefix"),
                    discord.SelectOption(label="Welcome Enabled", value="welcome_enabled"),
                ],
                custom_id="config_menu"
            )
        )

@bot.tree.command(name="settings", description="Interactive config menu")
async def settings(interaction: discord.Interaction):
    manager = ServerDataManager(interaction.guild)
    await interaction.response.send_message("Choose a setting:", view=ConfigMenu(manager), ephemeral=True)
