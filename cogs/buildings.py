from discord.ext import commands
from discord import app_commands, Interaction
from utils.embeds import building_to_embed

class Buildings(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="building", description="Look up a building by name")
    async def building(self, interaction: Interaction, name: str, level: int | None = None):
        await interaction.response.defer(thinking=True, ephemeral=False)
        b = self.bot.ds.get_building(name)
        if not b: return await interaction.followup.send(f"Could not find building **{name}**.")
        canon = next((k for k,v in self.bot.ds.data.get('buildings',{}).items() if v is b), name)
        await interaction.followup.send(embed=building_to_embed(canon, b, level))
async def setup(bot): await bot.add_cog(Buildings(bot))
