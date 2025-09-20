from __future__ import annotations

from discord import Interaction, app_commands
from discord.ext import commands

from utils.embeds import research_to_embed


class Research(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="research", description="Look up a research item")
    async def research(self, interaction: Interaction, name: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=False)

        match = self.bot.ds.lookup_research(name)
        if not match:
            await interaction.followup.send(f"No research found for **{name}**.")
            return

        canonical_name, research_item = match
        await interaction.followup.send(embed=research_to_embed(canonical_name, research_item))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Research(bot))
