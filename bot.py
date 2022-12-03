from dotenv import load_dotenv


load_dotenv()

from discord import Client, Intents, Message

from os import environ

bot = Client(intents=Intents.all())


@bot.event
async def on_ready():
    print("The bot is ready")


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    print(message)
    await message.reply("Hello, welcome to our server!")


bot.run(environ.get("BOT_TOKEN"))
