from discord.ext import commands
from discord import app_commands, Interaction
from utils.embeds import hero_to_embed

class Heroes(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="hero", description="Look up a hero by name")
    async def hero(self, interaction: Interaction, name: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        h = self.bot.ds.get_hero(name)
        if not h: return await interaction.followup.send(f"Could not find hero **{name}**.")
        canon = next((k for k,v in self.bot.ds.data.get('heroes',{}).items() if v is h), name)
        await interaction.followup.send(embed=hero_to_embed(canon, h))
async def setup(bot): await bot.add_cog(Heroes(bot))
