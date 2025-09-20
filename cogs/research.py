from discord.ext import commands
from discord import app_commands, Interaction
from utils.embeds import research_to_embed

class Research(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="research", description="Look up a research item")
    async def research(self, interaction: Interaction, name: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        r = self.bot.ds.get_research(name)
        if not r: return await interaction.followup.send(f"No research found for **{name}**.")
        canon = next((k for k,v in self.bot.ds.data.get('research',{}).items() if v is r), name)
        await interaction.followup.send(embed=research_to_embed(canon, r))
async def setup(bot): await bot.add_cog(Research(bot))
