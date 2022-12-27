from os import environ

from discord import Intents, Interaction, Object, Member, app_commands, Permissions
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
@app_commands.checks.has_permissions(ban_members=True)
async def kick_user(interaction: Interaction, user: Member):
    await interaction.response.defer()
    await interaction.guild.kick(user=Object(id=user.id))
    await interaction.followup.send(f"{interaction.user.name} has been **KICKED**!")


@bot.tree.command(name="ban_word", guild=guild)
async def ban_word(interaction: Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.name}!")


@bot.tree.command(name="unban_word", guild=guild)
async def unban_word(interaction: Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.name}!")


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

if __name__ == "__main__":
    bot.run(environ.get("BOT_TOKEN"))
