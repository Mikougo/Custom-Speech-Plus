import json
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COMMANDS_FILE = "commands.json"
RESERVED_COMMANDS = {"addcmd", "editcmd", "delcmd", "cmds", "help"}

# In-memory cache
custom_commands = {}

# Simple cooldown for custom text triggers
user_cooldowns = {}
CUSTOM_COMMAND_COOLDOWN = 2.0  # seconds


# ---------- FILE HANDLING ----------
def load_commands():
    global custom_commands

    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            custom_commands = data if isinstance(data, dict) else {}
    except FileNotFoundError:
        custom_commands = {}
    except json.JSONDecodeError:
        custom_commands = {}


def save_commands():
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_commands, f, indent=4, ensure_ascii=False)


# ---------- PERMISSION CHECK ----------
def can_manage_commands(ctx):
    if ctx.guild is None:
        return False

    if ctx.author.id == ctx.guild.owner_id:
        return True

    return ctx.author.guild_permissions.administrator


# ---------- HELPERS ----------
def split_message_chunks(lines, limit=1900):
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > limit:
            if current:
                chunks.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line

    if current:
        chunks.append(current)

    return chunks


def is_on_cooldown(user_id):
    now = time.time()
    last_used = user_cooldowns.get(user_id, 0)

    if now - last_used < CUSTOM_COMMAND_COOLDOWN:
        return True

    user_cooldowns[user_id] = now
    return False


# ---------- EVENTS ----------
@bot.event
async def on_ready():
    load_commands()
    print(f"Logged in as {bot.user}")
    print(f"Loaded {len(custom_commands)} custom command(s).")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Let built-in commands like !addcmd, !editcmd, !cmds work
    await bot.process_commands(message)

    # Only then check custom triggers
    content = message.content.strip()
    if not content.startswith("!"):
        return

    trigger = content[1:].strip().lower()

    # Prevent custom commands from shadowing management commands
    if trigger in RESERVED_COMMANDS:
        return

    if trigger in custom_commands:
        if is_on_cooldown(message.author.id):
            return

        await message.channel.send(custom_commands[trigger])


# ---------- ADD COMMAND ----------
@bot.command()
async def addcmd(ctx, *, content):
    if not can_manage_commands(ctx):
        await ctx.send("You need Administrator permission to add commands.")
        return

    if "=" not in content:
        await ctx.send("Usage: !addcmd trigger = response")
        return

    name, response = content.split("=", 1)
    name = name.strip().lower()
    response = response.strip()

    if not name or not response:
        await ctx.send("Command trigger and response cannot be empty.")
        return

    if name in RESERVED_COMMANDS:
        await ctx.send("That trigger is reserved.")
        return

    if name in custom_commands:
        await ctx.send("Command already exists. Use !editcmd to change it.")
        return

    custom_commands[name] = response
    save_commands()

    await ctx.send(f"Added command: !{name}")


# ---------- EDIT COMMAND ----------
@bot.command()
async def editcmd(ctx, *, content):
    if not can_manage_commands(ctx):
        await ctx.send("You need Administrator permission to edit commands.")
        return

    if not custom_commands:
        await ctx.send("There are no custom commands to edit.")
        return

    if "-" not in content:
        await ctx.send(
            "Usage:\n"
            "!editcmd old trigger = new trigger - old response = new response\n"
            "!editcmd old trigger = new trigger -\n"
            "!editcmd - old response = new response"
        )
        return

    trigger_part, response_part = content.split("-", 1)
    trigger_part = trigger_part.strip()
    response_part = response_part.strip()

    old_trigger = None
    new_trigger = None
    old_response = None
    new_response = None

    # ----- trigger edit part -----
    if trigger_part:
        if "=" not in trigger_part:
            await ctx.send("Invalid trigger format. Use: old trigger = new trigger")
            return

        old_trigger, new_trigger = trigger_part.split("=", 1)
        old_trigger = old_trigger.strip().lower()
        new_trigger = new_trigger.strip().lower()

        if not old_trigger or not new_trigger:
            await ctx.send("Trigger names cannot be empty.")
            return

        if old_trigger not in custom_commands:
            await ctx.send("That old trigger does not exist.")
            return

        if new_trigger in RESERVED_COMMANDS:
            await ctx.send("That new trigger is reserved.")
            return

        if new_trigger != old_trigger and new_trigger in custom_commands:
            await ctx.send("That new trigger already exists.")
            return

    # ----- response edit part -----
    if response_part:
        if "=" not in response_part:
            await ctx.send("Invalid response format. Use: old response = new response")
            return

        old_response, new_response = response_part.split("=", 1)
        old_response = old_response.strip()
        new_response = new_response.strip()

        if not old_response or not new_response:
            await ctx.send("Responses cannot be empty.")
            return

    if not trigger_part and not response_part:
        await ctx.send("You need to change at least the trigger or the response.")
        return

    # Response only
    if not trigger_part and response_part:
        matches = [
            trigger for trigger, response in custom_commands.items()
            if response == old_response
        ]

        if len(matches) == 0:
            await ctx.send("No command found with that old response.")
            return

        if len(matches) > 1:
            await ctx.send("Multiple commands have that response. Edit by trigger instead.")
            return

        target_trigger = matches[0]
        custom_commands[target_trigger] = new_response
        save_commands()

        await ctx.send(f"Updated response for !{target_trigger}")
        return

    # Trigger only
    if trigger_part and not response_part:
        custom_commands[new_trigger] = custom_commands.pop(old_trigger)
        save_commands()

        await ctx.send(f"Updated trigger: !{old_trigger} -> !{new_trigger}")
        return

    # Trigger + response
    current_response = custom_commands[old_trigger]

    if current_response != old_response:
        await ctx.send("Old response does not match that trigger.")
        return

    custom_commands.pop(old_trigger)
    custom_commands[new_trigger] = new_response
    save_commands()

    await ctx.send(f"Updated command: !{old_trigger} -> !{new_trigger}")


# ---------- DELETE COMMAND ----------
@bot.command()
async def delcmd(ctx, *, name):
    if not can_manage_commands(ctx):
        await ctx.send("You need Administrator permission to delete commands.")
        return

    name = name.strip().lower()

    if name not in custom_commands:
        await ctx.send("That command does not exist.")
        return

    del custom_commands[name]
    save_commands()

    await ctx.send(f"Deleted command: !{name}")


# ---------- LIST COMMANDS ----------
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cmds(ctx):
    if not custom_commands:
        await ctx.send("No custom commands exist yet.")
        return

    lines = [
        f"!{name} -> {response}"
        for name, response in sorted(custom_commands.items())
    ]

    chunks = split_message_chunks(lines)

    for chunk in chunks:
        await ctx.send(f"```{chunk}```")


# ---------- ERROR HANDLER ----------
@cmds.error
async def cmds_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Slow down bro 😭 try again in {error.retry_after:.1f}s")


# ---------- RUN ----------
if not TOKEN:
    raise ValueError("DISCORD_TOKEN is missing.")

bot.run(TOKEN)
