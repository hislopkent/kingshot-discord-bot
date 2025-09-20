from __future__ import annotations

from discord import Interaction, app_commands
from discord.ext import commands

from utils.embeds import hero_to_embed


class Heroes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="hero", description="Look up a hero by name")
    async def hero(self, interaction: Interaction, name: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=False)

        match = self.bot.ds.lookup_hero(name)
        if not match:
            await interaction.followup.send(f"Could not find hero **{name}**.")
            return

        canonical_name, hero = match
        await interaction.followup.send(embed=hero_to_embed(canonical_name, hero))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Heroes(bot))
