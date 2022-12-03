from os import environ

from discord import Intents, Interaction, Object
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

intents = Intents.default()

bot = Bot(command_prefix="!", intents=intents)

guild = Object(id=1043859468447911976)


@bot.event
async def on_ready():
    print("The bot is ready")
    await bot.tree.sync(guild=guild)


@bot.tree.command(name="hello", guild=guild)
async def hello(interaction: Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.name}!")


bot.run(environ.get("BOT_TOKEN"))
