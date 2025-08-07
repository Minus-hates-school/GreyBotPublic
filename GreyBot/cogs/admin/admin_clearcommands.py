import logging
from discord.ext import commands
from discord import app_commands
import discord
logger = logging.getLogger(__name__)
class AdminClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="clear",description="erase ALL commands in server")
    @app_commands.checks.has_permissions(administrator=True)
    async def AdminClearCommand(self,interaction: discord.Interaction):
        server = interaction.guild
        logger.info(f"Admin Clear called by {interaction.user} in {server}")
        bot = self.bot
        guild = interaction.guild
        channel = interaction.channel
        try:
            await bot.tree.clear_commands(guild=guild)
            await bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            try:
                await channel.send(f"Commands Have been cleared.")
            except Exception as e:
                logger.error(e)
        except Exception as e:
            await interaction.response.send_message(f"Commands were unable to be Synced..., {e}", ephemeral=True)
        await interaction.delete_original_response()

    @AdminClearCommand.error
    async def AdminError(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(AdminClear(bot))




