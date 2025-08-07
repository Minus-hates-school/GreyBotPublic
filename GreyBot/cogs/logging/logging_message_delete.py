"""
logs when a message is deleted.
"""
from datetime import datetime
import logging
import discord
from discord.ext import commands

from GreyBot.utils.interactions._embeds import embed_message_delete

logger = logging.getLogger(__name__)


class LoggingMessageDelete(commands.Cog):
    """
    Simple listener to on_message_delete
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        If a mod deletes, take the audit log event. If a user deletes, handle it normally.
        """
        # Don't record edits in Staff only channels.
        if message.channel == 1366812060058521700:  # This is the ID of the "staff area" category.
            # Yes, that's hardcoded. Suck it.
            return
        if message.author == self.bot.user:
            return
        current_guild = message.guild
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]
        logs_channel = await self.bot.fetch_channel("1394474643431362562")
        backup = await self.bot.fetch_channel("1394473942537994363")
        # If the audit log is triggered, it means someone OTHER than the author deleted the message.
        # https://discordpy.readthedocs.io/en/stable/api.html?highlight=audit%20log#discord.AuditLogAction.message_delete
        print(audit_log)
        print(f"Action: {audit_log.action}")
        print(f"After: {audit_log.after}")
        print(f"Before: {audit_log.before}")
        print(f"CAT: {audit_log.category}")
        print(f"Changes {audit_log.changes}")
        print(f"Created @: {audit_log.created_at}")
        print(f"extra: {audit_log.extra}")
        print(f"Guild: {audit_log.guild}")
        print(f"Id: {audit_log.id}")
        print(f"reason: {audit_log.reason}")
        print(f"Target: {audit_log.target}")
        print(f"User: {audit_log.user}")

        if str(audit_log.action) == 'AuditLogAction.message_delete':
            # Then a moderator deleted a message.
            embed = embed_message_delete(message.author, message, audit_log.user)
            await logs_channel.send(embed=embed)
            await backup.send(embed=embed)
        else:
            # Otherwise, the author deleted it.
            username = message.author
            await logs_channel.send(f"{username.mention}", embed=embed_message_delete(username, message))
            await backup.send(f"{username.mention}", embed=embed_message_delete(username, message))

async def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    await bot.add_cog(LoggingMessageDelete(bot))
