from discord.ext import commands
from discord import app_commands, Interaction
from utils.embeds import event_to_embed

class Events(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="event", description="List events or show one")
    async def event(self, interaction: Interaction, name: str | None = None):
        await interaction.response.defer(thinking=True, ephemeral=False)
        if name:
            ev = self.bot.ds.get_event(name)
            if not ev: return await interaction.followup.send(f"No event found for **{name}**.")
            canon = next((k for k,v in self.bot.ds.data.get('events',{}).items() if v is ev), name)
            return await interaction.followup.send(embed=event_to_embed(canon, ev))
        names = list(self.bot.ds.list_events() or [])
        return await interaction.followup.send("**Events:** " + (", ".join(sorted(names)) if names else "None"))
async def setup(bot): await bot.add_cog(Events(bot))
