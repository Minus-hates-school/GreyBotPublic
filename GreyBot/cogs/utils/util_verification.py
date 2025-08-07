import logging
from discord.ext import commands
import discord
from discord import app_commands
from GreyBot.utils.interactions import _embeds
import random
import string

logger = logging.getLogger(__name__)

grant_role = 1366814596274589857
application_channel = 1374422402347307109
applicant_reviwer_role = 1389671861390147716

class VerifyInputModal(discord.ui.Modal, title="Welcome to the interview process"):
    Question1 = discord.ui.TextInput(label="What is your current age?",
                                    placeholder="3",
                                    style=discord.TextStyle.short,
                                    required=True,
                                    max_length=3,
                                    min_length=2)
    Question2 = discord.ui.TextInput(label="what tool or service do you use in game",
                                    style=discord.TextStyle.short,
                                    required=True,
                                    max_length=100)
    Question3 = discord.ui.TextInput(label="How long have you been playing grey hack?",
                                     style=discord.TextStyle.short,
                                     required=True,
                                     max_length=100)
    Question4 = discord.ui.TextInput(label="Why do you wish to be an agent?",
                                     style=discord.TextStyle.short,
                                     required=True,
                                     max_length=100)
    Question5 = discord.ui.TextInput(label="What type of services do you wish to work in?",
                                     style=discord.TextStyle.short,
                                     required=True,
                                     max_length=100)

    def __init__(self, cog, interaction_user):
        super().__init__()
        self.cog = cog
        self.user = interaction_user

    async def on_submit(self, interaction: discord.Interaction):
        self.cog.author = self.user
        await interaction.response.defer(thinking=False)
        embed = discord.Embed(title="New Application Submission", color=discord.Color.green())
        embed.set_author(name=str(self.user), icon_url=self.user.display_avatar.url)
        embed.add_field(name="Age", value=self.Question1.value, inline=False)
        embed.add_field(name="Tools/Services Used", value=self.Question2.value, inline=False)
        embed.add_field(name="Time Playing Grey Hack", value=self.Question3.value, inline=False)
        embed.add_field(name="Why Become an Agent?", value=self.Question4.value, inline=False)
        embed.add_field(name="Service Interests", value=self.Question5.value, inline=False)
        embed.set_footer(text=f"User ID: {self.user}")
        try:
            channel = await self.cog.bot.fetch_channel(application_channel)
            thread = await channel.create_thread(
                name=''.join(random.choices(string.ascii_letters, k=6)).capitalize(),
                type=discord.ChannelType.private_thread,
            )
            await thread.add_user(self.user)
            await thread.send(f"<@&{applicant_reviwer_role}>",embed=embed)
            source_channel = await self.cog.bot.fetch_channel("1402362554701058240")
            original_msg = await source_channel.fetch_message("1402362618445959380")
            await thread.send(content=f"<@{self.user.id}> {original_msg.content}")
        except Exception as e:
            logger.warning(f"{e}")


class AdminVerifyModal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.author = None
        self.embed = None

    @app_commands.command(name="apply", description="start application process.")
    async def verify_post(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(grant_role)
        member = interaction.guild.get_member(interaction.user.id)
        if role in member.roles:
            await interaction.response.send_message(f"Well excuse me but you are already hired. don't do that again",ephemeral=True)
        else:
            await interaction.response.send_modal(VerifyInputModal(self, interaction.user))
            await interaction.followup.send(f"Application submitted. respond to the scenario now!",ephemeral=True)
async def setup(bot):
    await bot.add_cog(AdminVerifyModal(bot))
