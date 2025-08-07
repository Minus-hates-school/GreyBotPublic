import logging
from discord.ext import commands
from discord import app_commands
from GreyBot.utils.interactions import _embeds
import discord
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)
class AdminListCommands(commands.Cog): # CHANGE NAME HERE
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="commands",description="Fetch list of commadnds for server") # CHANGE NAME HERE
    async def AdminList(self,interaction: discord.Interaction):
        logger.info(f"{interaction.user} Called List Commands")
        cmds = interaction.client.tree.get_commands()
        msg = "\n".join([f"/{cmd.name} - {cmd.description}" for cmd in cmds])
        await interaction.response.send_message(f"Loaded Commands:\n```{msg}```", ephemeral=True)

async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(AdminListCommands(bot)) # CHANGE ADD HERE