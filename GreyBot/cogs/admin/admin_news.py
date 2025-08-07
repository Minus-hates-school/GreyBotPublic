import logging
from discord.ext import commands
import discord
from discord import app_commands
from GreyBot.utils.interactions import _embeds

logger = logging.getLogger(__name__)

class NewsInputModal(discord.ui.Modal, title="Post News Artical"):
    Title = discord.ui.TextInput(label="Post Title",placeholder="Website Seizure",style=discord.TextStyle.short,required=True,max_length=35,min_length=1)
    Focus = discord.ui.TextInput(label="Focus / target",style=discord.TextStyle.short,required=True,max_length=50)
    Body = discord.ui.TextInput(label="Body", style=discord.TextStyle.paragraph, required=True,max_length=750)


    def __init__(self, cog, interaction_user):
        super().__init__()
        self.cog = cog
        self.user = interaction_user


    async def on_submit(self, interaction: discord.Interaction):
        self.cog.author = self.user
        await interaction.response.defer(thinking=True)
        embed = discord.Embed(title=f":newspaper:{self.Title}",color=discord.Color.dark_red())
        embed.add_field(name=self.Focus,value=self.Body)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1366889384208629897/1366889504832622603/mZ2kyXx.png?ex=688894cd&is=6887434d&hm=b8ca02967c9d555c46d164570c47bc8d6fbd505d32409a100ca049f194eb6580&")
        embed.set_footer(text=f"post by {self.user}")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("News has been posted",ephemeral=True)


class AdminNewsModal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.author = None

    @app_commands.command(name="news", description="Create a News post from given Modal")
    async def news_post(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NewsInputModal(self, interaction.user))

async def setup(bot):
    await bot.add_cog(AdminNewsModal(bot))
