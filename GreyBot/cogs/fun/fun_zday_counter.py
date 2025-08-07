import logging
from discord.ext import commands
from discord import app_commands
import discord
from typing import Optional
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
SECONDS_PER_INGAME_MIN = 4.285714285714286
SECONDS_PER_INGAME_SECOND = SECONDS_PER_INGAME_MIN / 60  # ≈ 0.0667
INGAME_SECONDS_PER_REAL_SECOND = 1 / SECONDS_PER_INGAME_SECOND
from GreyBot.assets import settings
class FunZDAYCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.REAL_WORLD_ANCHOR = datetime.strptime(settings.load_setting("game","realworld"), "%B %d, %Y %H:%M")
        self.INGAME_ANCHOR = datetime.strptime(settings.load_setting("game","ingame"), "%B %d, %Y %H:%M")
        self.ZDAY_MONTHS = ['February', 'April', 'June', 'August', 'October', 'December']
        logger.info(f"loaded RWA: {self.REAL_WORLD_ANCHOR} IGA: {self.INGAME_ANCHOR}")

    def calculate_next_zday(self,ingame_time: datetime) -> datetime:
        ZDAY_MONTHS = self.ZDAY_MONTHS
        """Find the next in-game Z-Day based on current in-game time."""
        month_name = ingame_time.strftime("%B")

        if month_name in ZDAY_MONTHS and ingame_time.day <= 15:
            return ingame_time.replace(day=1, hour=0, minute=0, second=0)

        # Else, find the next even month from current position
        for i in range(1, 13):
            next_month = (ingame_time.month + i - 1) % 12 + 1
            year_shift = (ingame_time.month + i - 1) // 12
            test_year = ingame_time.year + year_shift
            test_date = datetime(test_year, next_month, 1)
            if test_date.strftime("%B") in ZDAY_MONTHS:
                return test_date

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
        return ingame_now.strftime('%B %d, %Y %H:%M')

    def UPDATE_ANCHORS(self):
        self.REAL_WORLD_ANCHOR = datetime.strptime(settings.load_setting("game","realworld"), "%B %d, %Y %H:%M")
        self.INGAME_ANCHOR = datetime.strptime(settings.load_setting("game","ingame"), "%B %d, %Y %H:%M")


    @app_commands.command(name="zday",description="zeroday counter") # CHANGE NAME HERE
    async def FunCounter(self,interaction: discord.Interaction, datetime: Optional[str]):
        """
           Parameters -----------
               datetime: Optional example: May 12, 2006 22:40 Leave blank to use current in game time.
        """
        logger.info(f"{interaction.user} Called for zday count with {datetime}")
        self.predict_ingame_from_now()
        try:
            ts = self.get_next_zday_real_time(self.predict_ingame_from_now())
            await interaction.response.send_message(f"Next Zero day <t:{ts}:F> <t:{ts}:R>")
        except Exception as c:
            logger.error(f"{c}")
            await interaction.response.send_message(f"Error. SOMTHING BAD HAS HAPPENED :( check your format",ephemeral=True)

    @commands.command(name="szday")
    @commands.is_owner()
    async def SyncZeroDay(self,ctx,*,newtime):
        now = datetime.now()
        settings.update_setting("game", "ingame",newtime)
        settings.update_setting("game", "realworld", now.strftime('%B %d, %Y %H:%M'))
        self.UPDATE_ANCHORS()
        await ctx.channel.send(f"Synced times to: {now.strftime('%B %d, %Y %H:%M')} --- {newtime}")

async def setup(bot):
    await bot.add_cog(FunZDAYCommands(bot)) # CHANGE ADD HERE

