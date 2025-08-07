import logging
from discord.ext import commands
from discord import app_commands
from GreyBot.utils.interactions import _embeds
import discord
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)
class AdminServerInfo(commands.Cog): # CHANGE NAME HERE
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sinfo",description="Fetch Server information for server") # CHANGE NAME HERE
    async def adminServerInfo(self,interaction: discord.Interaction):
        server = interaction.guild
        channel = interaction.channel
        users = server.member_count
        created = server.created_at
        dt = datetime.fromisoformat(str(created))
        clean = dt.strftime("%Y-%m-%d %H:%M:%S")
        data = f"Members: {users}\nCreated: {clean}"
        embed = _embeds.embed_default_response(title=server,content=data)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(AdminServerInfo(bot)) # CHANGE ADD HERE