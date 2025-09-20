from discord.ext import commands
from discord import app_commands, Interaction

class Admin(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="admin_reload", description="Reload JSON data from disk")
    async def admin_reload(self, interaction: Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            return await interaction.response.send_message("Need Manage Server permission.", ephemeral=True)
        await interaction.response.defer(thinking=True, ephemeral=True)
        await self.bot.ds.load_all()
        await interaction.followup.send("Reloaded data.")
async def setup(bot): await bot.add_cog(Admin(bot))
