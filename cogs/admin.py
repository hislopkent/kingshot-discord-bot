from __future__ import annotations

from discord import Interaction, app_commands
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="admin_reload", description="Reload JSON data from disk")
    async def admin_reload(self, interaction: Interaction) -> None:
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("Need Manage Server permission.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True, ephemeral=True)
        await self.bot.ds.load_all()
        await interaction.followup.send("Reloaded data.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
