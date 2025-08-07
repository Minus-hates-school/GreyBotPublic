import logging
import time

import aiohttp.connector


def unix_time() -> str: return f"<t:{(int(time.time()))}>"
from discord.ext import commands
logger = logging.getLogger(__name__)
class AdminShutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="shutdown",description="erase Messages by number or id")
    @commands.is_owner()  # Optional: only allow the bot owner to run this
    async def AdminShutdownCommand(self,ctx):
        logger.info(f"Admin Shutdown called by {ctx.author} in {ctx.guild}")
        bot = self.bot
        await ctx.send(f"Shutting down... {unix_time()}")
        try:
            await bot.close()
        except Exception as e:
            logger.error(f"Cant Close Bot session: {e}")

    @AdminShutdownCommand.error
    async def AdminShutdown(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator to use this command.")
async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(AdminShutdown(bot))




