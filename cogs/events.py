from __future__ import annotations

from discord import Interaction, app_commands
from discord.ext import commands

from utils.embeds import event_to_embed


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="event", description="List events or show one")
    async def event(self, interaction: Interaction, name: str | None = None) -> None:
        await interaction.response.defer(thinking=True, ephemeral=False)

        if name:
            match = self.bot.ds.lookup_event(name)
            if not match:
                await interaction.followup.send(f"No event found for **{name}**.")
                return

            canonical_name, event = match
            await interaction.followup.send(embed=event_to_embed(canonical_name, event))
            return

        names = self.bot.ds.list_events()
        listing = ", ".join(names) if names else "None"
        await interaction.followup.send(f"**Events:** {listing}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
