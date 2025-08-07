import json
import logging
import discord
from discord.ext import commands
from discord import app_commands
from discord import embeds
import requests
from bs4 import BeautifulSoup as BS
logger = logging.getLogger(__name__)
class GeneralSteamLookup(commands.Cog):
    """
    # This cog can be used as a template for any command.
    """
    def __init__(self, bot):
        self.bot = bot

    def SteamNameToId(self,Steam_User):
        url = f"https://steamid.io/lookup/{Steam_User}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BS(response.text,"html.parser")
            data = soup.find("a",{'data-steamid64':True})
            if data:
                id = (data["data-steamid64"])
                print(f"SteamID: {id}")
                return id
            else:
                logger.warning(f"Failed to find steam id at {url}")
                return False
        else:
            logger.warning(f"Failed to fetch page. Status code: {response.status_code}")
            return False

    def Steam64ToSteam2(self,steamid64):
        steamid64 = int(steamid64)
        y = steamid64 % 2
        z = (steamid64 - 76561197960265728 - y) // 2
        return f"STEAM_0:{y}:{z}"

    def Embed(self,data):
        ignore = ['private',"PRIVATE","Private","Not set","profile",'steamID64 (Hex)','steamID3','steamID']
        embed = discord.Embed(
            title=f'Steam Data for {data["name"]}'
            ,color=discord.Color.dark_grey()
        )
        for x,y in data.items():
            if y in ignore or x in ignore:
                pass
            else:
                embed.add_field(name=x,value=y,inline=False)

        embed.set_thumbnail(
            url=data["profile"]
        )
        return embed
    def DataFromSteamID(self,id):
        url = f"https://www.steamidfinder.com/lookup/{id}/"
        headers = {"User-Agent": "Mozilla/4.7 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BS(response.text, "html.parser")
            profile_info = soup.find("table", id="profile-info")
            data = {}
            for row in profile_info.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    label = th.text.strip().rstrip(":")
                    if td.code and td.code.a:
                        value = td.code.a['href']  # if it's a link
                    else:
                        value = td.text.strip()
                    data[label] = value
        return data
    @app_commands.command(name="steamid", description="Look Up someones steam id by the name on profile.")
    async def steam_lookup(self, interaction: discord.Interaction, name: str):
        t = self.SteamNameToId(name)
        if not t or t == None:
            return "name not found"
        await interaction.response.send_message(embed=self.Embed(self.DataFromSteamID(id=t)))

async def setup(bot):
    """
    Required.
    """
    try:
        await bot.add_cog(GeneralSteamLookup(bot))
    except app_commands.CommandAlreadyRegistered:
        return










