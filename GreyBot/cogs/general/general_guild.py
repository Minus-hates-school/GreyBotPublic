import logging
import discord
from discord.ext import commands
from discord import app_commands
logger = logging.getLogger(__name__)

class GeneralGuild(commands.Cog):
    """
    # This cog can be used as a template for any command.
    """
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="guild",description="Returns Current Guild information")
    async def guild_info(self,interaction: discord.Interaction):
        guild = interaction.guild
        if guild:
            await interaction.response.send_message(f"Guild: **{guild.name}**\nID: `{guild.id}`")
        else:
            await interaction.response.send_message("This command must be run in a server.")

async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(GeneralGuild(bot))



