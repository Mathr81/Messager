import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name = "ping", description="Sends the bot's latency.")
async def ping(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.send_message(f"Pong! Latency is {round(bot.latency * 1000)}ms")

# create a slashcommand to send a message as the bot
@bot.slash_command(name = "send", description="Sends a message as the bot.")
async def send(interaction: disnake.ApplicationCommandInteraction, message: str):
    if await check_staff_role(interaction):
        await interaction.channel.send(message)
        await interaction.response.send_message(f"Sent message: `{message}`", ephemeral=True)

# create a slashcommand to edit a message sent by the bot
@bot.slash_command(name = "edit", description="Edits a message sent by the bot.")
@commands.has_role(os.getenv("STAFF_ROLE")) # only allow staff members to use this command
async def edit(interaction: disnake.ApplicationCommandInteraction, message_id: str, message: str):
    if await check_staff_role(interaction):
        message_to_edit = await interaction.channel.fetch_message(message_id)
        await message_to_edit.edit(content=message)
        await interaction.response.send_message(f"Edited message: `{message}`", ephemeral=True)

# create a slashcommand to delete a message sent by the bot
@bot.slash_command(name = "delete", description="Deletes a message sent by the bot.")
async def delete(interaction: disnake.ApplicationCommandInteraction, message_id: str):
    if await check_staff_role(interaction):
        message_to_delete = await interaction.channel.fetch_message(message_id)
        await message_to_delete.delete()
        await interaction.response.send_message(f"Deleted message: `{message_to_delete.content}`", ephemeral=True)

# create a slashcommand to reply to a message as the bot
@bot.slash_command(name = "reply", description="Replies to a message as the bot.")
async def reply(interaction: disnake.ApplicationCommandInteraction, message_id: str, message: str):
    if await check_staff_role(interaction):
        message_to_reply = await interaction.channel.fetch_message(message_id)
        await message_to_reply.reply(message)
        await interaction.response.send_message(f"Replied to message: `{message_to_reply.content}`", ephemeral=True)

# create a slashcommand to react to a message as the bot
@bot.slash_command(name = "react", description="Reacts to a message as the bot.")
async def react(interaction: disnake.ApplicationCommandInteraction, message_id: str, emoji: str):
    if await check_staff_role(interaction):
        message_to_react = await interaction.channel.fetch_message(message_id)
        await message_to_react.add_reaction(emoji)
        await interaction.response.send_message(f"Reacted to message: `{message_to_react.content}`", ephemeral=True)

# create a slashcommand to unreact to a message as the bot
@bot.slash_command(name = "unreact", description="Unreacts to a message as the bot.")
async def unreact(interaction: disnake.ApplicationCommandInteraction, message_id: str, emoji: str):
    if await check_staff_role(interaction):
        message_to_unreact = await interaction.channel.fetch_message(message_id)
        await message_to_unreact.remove_reaction(emoji, interaction.user)
        await interaction.response.send_message(f"Unreacted to message: `{message_to_unreact.content}`", ephemeral=True)

async def check_staff_role(interaction: disnake.ApplicationCommandInteraction):
    if interaction.user.roles and os.getenv("STAFF_ROLE") not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message("You must be a staff member to use this command.", ephemeral=True)
        return False
    return True

# create a help slashcommand to display help information

@bot.slash_command(name = "help", description="Display help information")
async def help(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.send_message("Please visit the [documentation](https://github.com/Mathr81/Messager/blob/main/doc.md) for all the commands", ephemeral=True)

bot.run(os.getenv('TOKEN'))