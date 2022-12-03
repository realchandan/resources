from os import environ

from discord import Intents, Message
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

intents = Intents.all()

bot = Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("The bot is ready")


@bot.command(name="hello")
async def hello(message: Message):
    print(message)
    await message.reply(f"Hello {message.author.name}!")


# @bot.event
# async def on_message(message: Message):
#     if message.author == bot.user:
#         return
#     print(message)
#     await message.reply("Hello, welcome to our server!")


bot.run(environ.get("BOT_TOKEN"))
