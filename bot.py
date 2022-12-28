from os import environ
from time import time
from typing import List

from discord import Intents, Interaction, Member, Message, Object, app_commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

from database import Violations, Word, db

load_dotenv()

intents = Intents.default()
intents.message_content = True

bot = Bot(command_prefix="!", intents=intents)

guild = Object(id=1043859468447911976)


@bot.event
async def on_ready():
    print("The bot is ready")
    await bot.tree.sync(guild=guild)


@bot.tree.command(
    name="ban_user",
    description="This command can be used to ban users",
    guild=guild,
)
@app_commands.describe(
    user="This is the user you wish to ban",
    reason="Please provide a description why the user is being banned",
)
@app_commands.checks.has_role(1056467619881959464)
@app_commands.checks.has_permissions(ban_members=True)
async def ban_user(
    interaction: Interaction, user: Member, reason: str = "No reason specified"
):
    await interaction.response.defer()
    await user.ban(reason=reason)
    await interaction.followup.send(
        f"{interaction.user.name} has been banned for -> {reason} this reason!"
    )


@bot.tree.command(name="unban_user", guild=guild)
@app_commands.checks.has_role(1056467619881959464)
@app_commands.checks.has_permissions(ban_members=True)
async def unban_user(interaction: Interaction, user_id: str):
    await interaction.response.defer()
    await interaction.guild.unban(
        user=Object(id=user_id), reason="Don't make the same mistake again! :)"
    )
    await interaction.followup.send(f"{interaction.user.name} has been unbanned!")


@bot.tree.command(name="kick_user", guild=guild)
@app_commands.checks.has_role(1056467619881959464)
@app_commands.checks.has_permissions(kick_members=True)
async def kick_user(interaction: Interaction, user: Member):
    await interaction.response.defer()
    await interaction.guild.kick(user=Object(id=user.id))
    await interaction.followup.send(f"{interaction.user.name} has been **KICKED**!")


@bot.tree.command(name="ban_word", guild=guild)
@app_commands.checks.has_role(1056467619881959464)
async def ban_word(interaction: Interaction, word: str):
    await interaction.response.defer()
    db.merge(Word(banned_word=word))
    db.commit()
    await interaction.followup.send(f"{word} has been **BANNED** from now on!")


@bot.tree.command(name="unban_word", guild=guild)
@app_commands.checks.has_role(1056467619881959464)
async def unban_word(interaction: Interaction, word: str):
    await interaction.response.defer()
    result = db.query(Word).filter(Word.banned_word == word).delete()
    db.commit()
    if result == 0:
        await interaction.followup.send(
            f"The given word is not banned thus no action taken!"
        )
        return
    await interaction.followup.send(f"{word} was **UNBANNED**")


async def _common_error_handler(interaction: Interaction, error):
    await interaction.response.defer()
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.followup.send(
            "You don't have **required permissions** to run this command!"
        )
        return
    if isinstance(error, app_commands.MissingRole):
        await interaction.followup.send(
            "You don't have **required roles** to run this command!"
        )
        return
    if isinstance(error, app_commands.NoPrivateMessage):
        await interaction.followup.send(
            "You can't run this command in a DM chat/private chat!"
        )
        return
    await interaction.followup.send("Something went wrong!")


ban_user.error(_common_error_handler)
unban_user.error(_common_error_handler)
kick_user.error(_common_error_handler)
ban_word.error(_common_error_handler)
unban_word.error(_common_error_handler)


@bot.event
async def on_message(message: Message):
    if bot.user == message.author:
        return

    banned_words: List[Word] = db.query(Word).all()
    message_has_violation = False
    violated_word = ""

    for x in banned_words:
        if x.banned_word in message.content:
            message_has_violation = True
            violated_word = x.banned_word
            break

    if message_has_violation:
        v = Violations()
        v.user_id = message.author.id
        v.timestamp = int(time())
        v.word = violated_word
        db.add(v)
        db.commit()

    results: List[Violations] = (
        db.query(Violations).filter(Violations.user_id == message.author.id).all()
    )
    if len(results) >= 3:
        await message.guild.kick(user=Object(id=message.author.id))
        await message.channel.send(
            f"<@{message.author.id}> has been **KICKED** because they have send more than 3 messages with violations!"
        )
        return

    if message_has_violation:
        await message.reply(
            f"<@{message.author.id}> You are **warned** to not use **{violated_word}** again!"
        )


if __name__ == "__main__":
    bot.run(environ.get("BOT_TOKEN"))
