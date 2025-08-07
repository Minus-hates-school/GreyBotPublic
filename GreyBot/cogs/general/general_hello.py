import logging
from discord.ext import commands
from discord import app_commands
import discord
import asyncio

logger = logging.getLogger(__name__)
class GeneralHello(commands.Cog): # CHANGE NAME HERE
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello",description="Say hello?") # CHANGE NAME HERE
    async def hello(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}", ephemeral=True)
        await asyncio.sleep(4)
        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            print("msg already deleted.")
async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(GeneralHello(bot)) # CHANGE ADD HERE
