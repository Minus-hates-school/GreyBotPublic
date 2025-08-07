import logging
from discord.ext import commands
from discord import app_commands
import discord
logger = logging.getLogger(__name__)
import time
def unix_time() -> str: return f"<t:{(int(time.time()))}>"
class AdminSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="sync",
                          description="sync commands within a sever/guild")
    @app_commands.default_permissions(discord.Permissions(administrator=True))
    @app_commands.checks.has_permissions(administrator=True)
    async def AdminSyncCommands(self,interaction: discord.Interaction):
        server = interaction.guild
        logger.info(f"Admin Sync called by {interaction.user} in {server}")
        channel = interaction.channel
        try:
            await interaction.response.send_message(f"Syncing Commands for guild {server}", ephemeral=True)
            await self.bot.tree.sync(guild=server)
            try:
                await channel.send(f"Server is synced. {unix_time()}")
            except Exception as e:
                logger.error(e)
        except Exception as e:
            await interaction.response.send_message(f"Commands were unable to be Synced..., {e}", ephemeral=True)
        await interaction.delete_original_response()

    @AdminSyncCommands.error
    async def AdminError(self,interaction: discord.Interaction, error):
        if isinstance(error,app_commands.MissingPermissions):
            logger.error(f"somebody tried to run a admin command... @{interaction.user}")
            await interaction.response.send_message("You must be an administrator to use this command.",ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminSync(bot))
