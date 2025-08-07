import logging
from discord.ext import commands
from discord import app_commands
from typing import Optional
import discord
logger = logging.getLogger(__name__)
class AdminPurge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_id = 0
        self.target_msg = 0
    @app_commands.command(name="purge",description="erase Messages by number or id")
    @app_commands.default_permissions(discord.Permissions(administrator=True))
    @app_commands.checks.has_permissions(administrator=True)
    async def AdminPurgeCommand(self,interaction: discord.Interaction, oldest: str, newest: Optional[str] = None):
        """
           Parameters -----------
               oldest: str
               first / oldest message ID of what you are trying to erase. also supports ints like 10 & 40

               newest: Optional[str]
               last or newest message of what you are trying to erase

           """
        logger.info(f"Admin Purge called by {interaction.user} in {interaction.guild}")
        oldest = int(oldest)
        try:
            await interaction.response.defer(ephemeral=True,thinking=True)
            logger.info(f"Admin Purge loadded {oldest} as a {type(oldest)}")
            messages = []
            if oldest < 1000:
                messages = [m async for m in interaction.channel.history(limit=oldest)]
            else:
                logger.info(f"Trying to load Up to message id: {oldest}")
                target_msg = discord.Object(id=int(oldest))
                self.target_msg = target_msg
                if not target_msg:
                    logger.error(f"Unable to find message id: {oldest}")
                    await interaction.followup.send("Message Id not found.",ephemeral=True)
                    return
                else:
                    logger.info(f"Purge command found requested message id: {target_msg}")

                if not newest:
                    async for msg in interaction.channel.history(limit=1):
                        self.last_id = discord.Object(id=int(msg.id))
                        logger.info(f"Loading last id: {self.last_id}")
                else:
                    self.last_id = discord.Object(id=int(newest))
                if not self.last_id:
                    logger.warning("Last Id Failed to load creating one now.")
                    msg = await interaction.channel.send("erasing that which once was...")
                    self.last_id = discord.Object(id=int(msg.id))
                    logger.info(msg)
                messages = [msg async for msg in interaction.channel.history(after=target_msg,before=self.last_id)]
            if not messages:
                logger.error("No Messages Found.")
                await interaction.followup.send_message("No messages found to purge")
                return
            recent = [m for m in messages if (discord.utils.utcnow() - m.created_at).days < 14]
            if len(recent) >= 2:
                logger.info(f"Bulk Delete oldested...")
                try:
                    await interaction.channel.delete_messages(recent)
                except Exception as f:
                    logger.error(f"Recent Bulk Delete failed: {f}")

            for msg in messages:
                try:
                    await msg.delete()
                except Exception as f:
                    if f == discord.NotFound:
                        logger.warning(f"Failed to delete {msg.id} {f}")

        except Exception as e:
            logger.critical(f"Purge Command Failed: {e}")
            await interaction.followup.send_message(f"{e}", ephemeral=True)
        finally:
            logger.info("Purge Command Completed.")
            await interaction.followup.send("whew... that was a lot", ephemeral=True)
            await interaction.channel.send("This channel has had a spiritual awakening")
    @AdminPurgeCommand.error
    async def AdminError(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
async def setup(bot):
    await bot.add_cog(AdminPurge(bot))