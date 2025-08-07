import logging
from discord.ext import commands
from GreyBot.helpers import helpers_server_add
import time
def unix_time() -> str: return str(time.time())
from discord import app_commands
import discord
import asyncio

logger = logging.getLogger(__name__)

class EventHandler(commands.Cog):
    """
    # This cog can be used as a template for any command.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        await self.bot.wait_until_ready()
        print(f"Bot is now ready for initializations..")
        for guild in bot.guilds:
            helpers_server_add.init_server(guild)
            try:
                # Sync globally (optional) takes 1 hour
                await bot.tree.sync()
                for guild in bot.guilds:
                    try:
                        await bot.tree.sync(guild=guild)
                        print(f"- {guild.name} (ID: {guild.id})")
                    except Exception as p:
                        logger.error(f"Error syncing {guild.name}: {p}")
                    try:
                        for cmd in bot.tree.get_commands(guild=guild):
                            print(f"   - /{cmd.name}: {cmd.description}")
                    except Exception as f:
                        logger.error(f"Error getting commands for  {guild.name}: {f}")

            except Exception as e:
                logger.error(f"Global sync failed: {e}")



    @commands.Cog.listener(name="on_message")
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        print(f"{message.guild} | #{message.channel} | @{message.author}: {message.content}")

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self,member):
        """~ Gives members the X role upon joining the server ~"""
        role_name = "X"
        role = discord.utils.get(member.guild.roles, name=role_name)
        age = (discord.utils.utcnow() - member.created_at).days
        if age < 7:
            channel_id = 1402687544495439982  # Replace with your channel ID for user joins or welcomes
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(f":warning:**Warning** <@&1389671861390147716> Newly created account detected: <@{member.id}>\n Manual Verification Required.")
            else:
                logger.error("Channel not found. Make sure the bot has access.")
        else:
            if role:
                try:
                    await member.add_roles(role)
                    logger.info(f"Gave {member} the '{role.name}' role.")
                except discord.Forbidden:
                    logger.critical("Bot lacks permission to assign roles.")
                except discord.HTTPException as e:
                    logger.warning(f"Failed to assign role: {e}")
            else:
                logger.error(f"Role '{role_name}' not found.")
async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(EventHandler(bot))
