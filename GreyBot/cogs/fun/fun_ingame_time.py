import time
from datetime import datetime, timedelta
import logging
from discord.ext import commands
from discord import app_commands
from GreyBot.utils.interactions import _embeds
import discord

from typing import Optional
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
SECONDS_PER_INGAME_MIN = 4.285714285714286
SECONDS_PER_INGAME_SECOND = SECONDS_PER_INGAME_MIN / 60  # ≈ 0.0667
INGAME_SECONDS_PER_REAL_SECOND = 1 / SECONDS_PER_INGAME_SECOND
from GreyBot.assets import settings
class FunInGameTimeCommands(commands.Cog): # CHANGE NAME HERE
    def __init__(self, bot):
        self.bot = bot
        self.REAL_WORLD_ANCHOR = datetime.strptime(settings.load_setting("game","realworld"), "%B %d, %Y %H:%M")
        self.INGAME_ANCHOR = datetime.strptime(settings.load_setting("game","ingame"), "%B %d, %Y %H:%M")
        logger.info(f"loaded RWA: {self.REAL_WORLD_ANCHOR} IGA: {self.INGAME_ANCHOR}")

    def ingame_to_real_time(self,target_ingame: datetime) -> datetime:
        """Convert an in-game timestamp to real-world time."""
        ingame_delta_seconds = (target_ingame - self.INGAME_ANCHOR).total_seconds()
        real_seconds = ingame_delta_seconds * SECONDS_PER_INGAME_SECOND
        return self.REAL_WORLD_ANCHOR + timedelta(seconds=real_seconds)

    def get_next_zday_real_time(self,current_ingame_str: str):
        """Main function to determine real-world time for next Z-Day."""
        fmt = "%B %d, %Y %H:%M"
        ingame_now = datetime.strptime(current_ingame_str, fmt)
        next_zday_ingame = self.calculate_next_zday(ingame_now)
        zday_real_time = self.ingame_to_real_time(next_zday_ingame)
        return int(zday_real_time.timestamp())

    def real_to_ingame_time(self,real_time: datetime) -> datetime:
        delta_real = (real_time - self.REAL_WORLD_ANCHOR).total_seconds()
        delta_ingame = delta_real * INGAME_SECONDS_PER_REAL_SECOND
        return self.INGAME_ANCHOR + timedelta(seconds=delta_ingame)

    def predict_ingame_from_now(self):
        now = datetime.now()
        ingame_now = self.real_to_ingame_time(now)
        logger.info(f"[Real Now    ]: {now.strftime('%B %d, %Y %H:%M')}")
        logger.info(f"[Predicted IG]: {ingame_now.strftime('%B %d, %Y %H:%M')} Unix: {int(ingame_now.timestamp())}")
        return ingame_now.strftime('%B %d, %Y %H:%M')

    @app_commands.command(name="tig",description="Provides User with the current in game time from nothing but basic math") # CHANGE NAME HERE
    async def FunCounter(self,interaction: discord.Interaction):
        try:
            await interaction.response.send_message(f"Server Clock: {self.predict_ingame_from_now()}")
        except Exception as c:
            logger.error(f"{c}")
            await interaction.response.send_message(f"Error. SOMTHING BAD HAS HAPPENED ",ephemeral=True)


async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(FunInGameTimeCommands(bot)) # CHANGE ADD HERE

