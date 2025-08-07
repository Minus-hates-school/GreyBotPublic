from typing import Any

import discord
from discord._types import ClientT
from discord.ext import commands
from discord import app_commands, Interaction

COLOR_ROLES = {
    "Red": 1402903716071215194,
    "Blue": 1402903829372211231,
    "Yellow": 1402903790683947029
}

REGION_ROLES = {
    "North America": 1402904207715205164,
    "Europe": 555555555555555555,
    "Asia": 1402904122872696872
}

## TESTING USE STATIC
## DEPLOYMENT USE SETTINGS FILE.
PING_ROLES = {
    "Event Pings": 1402903963057262643,
    "Giveaway Pings": 888888888888888888,
    "Announcement Pings": 999999999999999999
}
class RoleDropdown(discord.ui.Select):
    def __init__(self, category_name, role_map: dict, user_roles: list[discord.Role]):
        self.category_name = category_name
        self.role_map = role_map

        options = []
        for label, role_id in role_map.items():
            is_selected = any(r.id == role_id for r in user_roles)
            options.append(discord.SelectOption(
                label=label,
                value=str(role_id),
                default=is_selected
            ))

        super().__init__(
            placeholder=f"Select {category_name}...",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id=f"{category_name.lower()}_select"
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        selected_ids = [int(v) for v in self.values]
        selected_roles = [guild.get_role(rid) for rid in selected_ids]
        all_roles = [guild.get_role(rid) for rid in self.role_map.values()]
        to_add = [r for r in selected_roles if r and r not in user.roles]
        to_remove = [r for r in all_roles if r in user.roles and r not in selected_roles]
        await user.add_roles(*to_add, reason=f"Self-assigned {self.category_name}")
        await user.remove_roles(*to_remove, reason=f"Self-removed {self.category_name}")
        await interaction.response.send_message(
            f"✅ Updated your **{self.category_name}** roles.", ephemeral=True
        )


class RoleView(discord.ui.View):
    def __init__(self,user_roles):
        super().__init__(timeout=None)
        self.add_item(RoleDropdown("Colors", COLOR_ROLES,user_roles))
        self.add_item(RoleDropdown("Regions", REGION_ROLES,user_roles))
        self.add_item(RoleDropdown("Pings", PING_ROLES,user_roles))


class FunRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roles",description="erase Messages by number or id")
    @app_commands.default_permissions(discord.Permissions(administrator=True))
    async def FunRolesCommand(self,interaction: discord.Interaction):
        user_roles = interaction.user.roles
        embed = discord.Embed(
            title="🎭 Self Role Selector",
            description="Select your roles using the dropdown menus below.\n\n"
                        "🎨 **Colors** – Choose a color role\n"
                        "🌍 **Regions** – Choose your region\n"
                        "🔔 **Pings** – Get notified for events, giveaways, or announcements",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=RoleView(user_roles),
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(FunRoles(bot))