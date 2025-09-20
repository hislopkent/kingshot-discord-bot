from __future__ import annotations

from discord import Interaction, app_commands
from discord.ext import commands

from utils.embeds import building_to_embed


class Buildings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="building", description="Look up a building by name")
    async def building(
        self, interaction: Interaction, name: str, level: int | None = None
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=False)

        match = self.bot.ds.lookup_building(name)
        if not match:
            await interaction.followup.send(f"Could not find building **{name}**.")
            return

        canonical_name, building = match
        await interaction.followup.send(embed=building_to_embed(canonical_name, building, level))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Buildings(bot))
