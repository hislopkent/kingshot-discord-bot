import os
import logging
import discord
from discord.ext import commands
from utils.datastore import DataStore
from utils.embeds import hero_embed, building_embed, research_embed, event_embed, links_embed

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("kingshot-bot")

INTENTS = discord.Intents.none()
BOT_PREFIX = "!"

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN in environment. See .env.example")

class KingshotBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=BOT_PREFIX, intents=INTENTS, **kwargs)
        self.ds = None

    async def setup_hook(self):
        self.ds = DataStore()
        await self.ds.load_all()

        for ext in ("cogs.heroes","cogs.buildings","cogs.research","cogs.events","cogs.admin"):
            try:
                await self.load_extension(ext)
                log.info("Loaded extension: %s", ext)
            except Exception as e:
                log.exception("Failed to load %s: %s", ext, e)

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

bot = KingshotBot()

@bot.tree.command(description="Quick links for Kingshot resources")
async def links(interaction: discord.Interaction):
    await interaction.response.defer(thinking=False, ephemeral=False)
    await interaction.followup.send(embed=links_embed(bot.ds))

@bot.tree.command(description="Ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.defer(thinking=False, ephemeral=True)
    await interaction.followup.send(f"Pong! Latency: {bot.latency*1000:.1f} ms")

bot.run(TOKEN)
