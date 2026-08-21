import discord
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os

from config import (
    TOKEN,
    CHANNEL_ID,
    REMINDER_USER_ID,
    TIMEZONE,
    REMINDER_HOUR,
    REMINDER_MINUTE
)


# ============================================================
# BOT SETUP
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ============================================================
# FILE
# ============================================================

EVENT_FILE = "events.json"


# ============================================================
# TIME
# ============================================================

def get_now():
    return datetime.now(
        ZoneInfo(TIMEZONE)
    )


def get_today():
    return get_now().strftime(
        "%Y-%m-%d"
    )


def get_week():
    return get_now().strftime(
        "%Y-W%U"
    )


def get_display_date():
    return get_now().strftime(
        "%d/%m/%Y"
    )


# ============================================================
# LOAD EVENTS
# ============================================================

def load_events():

    if not os.path.exists(EVENT_FILE):

        print("ERROR: events.json not found.")

        return {
            "alliance": {},
            "lsm": {}
        }

    try:

        with open(
            EVENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"ERROR loading events.json: {error}"
        )

        return {
            "alliance": {},
            "lsm": {}
        }


# ============================================================
# ALLIANCE EVENT
# ============================================================

def make_alliance_event():

    data = load_events()

    alliance = data.get(
        "alliance",
        {}
    )

    today = get_today()

    # --------------------------------------------------------
    # Get today's Alliance event
    # --------------------------------------------------------

    event = alliance.get(
        today
    )

    # --------------------------------------------------------
    # If today's event isn't specifically configured,
    # use the default Alliance event.
    # --------------------------------------------------------

    if event is None:

        event = alliance.get(
            "default"
        )

    # --------------------------------------------------------
    # No event
    # --------------------------------------------------------

    if event is None:

        return (
            "🚨 **ALLIANCE EVENT** 🚨\n\n"
            f"📅 **Date:** {get_display_date()}\n\n"
            "❌ No Alliance Event has been configured "
            "for today."
        )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location = event.get(
        "location",
        "Not specified"
    )

    # --------------------------------------------------------
    # Units
    # --------------------------------------------------------

    units = event.get(
        "units",
        []
    )

    # --------------------------------------------------------
    # Build message
    # --------------------------------------------------------

    message = (
        "🚨 **ALLIANCE EVENT** 🚨\n\n"
        f"📅 **Date:** {get_display_date()}\n"
        f"📍 **Location:** {location}\n\n"
        "🚒 **UNITS TO SEND:**\n"
    )

    if not units:

        message += (
            "No units have been configured."
        )

    else:

        for unit in units:

            message += (
                f"• {unit}\n"
            )

    message += (
        "\n━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Alliance deployment information."
    )

    return message


# ============================================================
# LSM
# ============================================================

def make_lsm_event():

    data = load_events()

    lsm = data.get(
        "lsm",
        {}
    )

    current_week = get_week()

    # --------------------------------------------------------
    # Get this week's LSM
    # --------------------------------------------------------

    event = lsm.get(
        current_week
    )

    # --------------------------------------------------------
    # If this week's LSM isn't specifically configured,
    # use the default.
    # --------------------------------------------------------

    if event is None:

        event = lsm.get(
            "default"
        )

    # --------------------------------------------------------
    # No LSM
    # --------------------------------------------------------

    if event is None:

        return (
            "🌪️ **LSM** 🌪️\n\n"
            f"📅 **Week:** {current_week}\n\n"
            "❌ No LSM has been configured "
            "for this week."
        )

    # --------------------------------------------------------
    # LSM TYPE
    # --------------------------------------------------------

    lsm_type = event.get(
        "type",
        "Not specified"
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    location = event.get(
        "location",
        "Not specified"
    )

    # --------------------------------------------------------
    # Build message
    # --------------------------------------------------------

    message = (
        "🌪️ **LSM** 🌪️\n\n"
        f"📋 **Type:** {lsm_type}\n"
        f"📍 **Location:** {location}\n\n"
        "This is this week's LSM."
    )

    return message


# ============================================================
# BUTTON VIEW
# ============================================================

class EventView(
    discord.ui.View
):

    def __init__(self):

        super().__init__(
            timeout=None
        )

    # ========================================================
    # ALLIANCE BUTTON
    # ========================================================

    @discord.ui.button(
        label="Alliance Event",
        style=discord.ButtonStyle.green,
        emoji="🚨",
        custom_id="event_alliance"
    )
    async def alliance_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            make_alliance_event(),
            ephemeral=True
        )

    # ========================================================
    # LSM BUTTON
    # ========================================================

    @discord.ui.button(
        label="LSM",
        style=discord.ButtonStyle.red,
        emoji="🌪️",
        custom_id="event_lsm"
    )
    async def lsm_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            make_lsm_event(),
            ephemeral=True
        )


# ============================================================
# DAILY REMINDER
# ============================================================

async def send_daily_reminder():

    # --------------------------------------------------------
    # Get channel
    # --------------------------------------------------------

    channel = bot.get_channel(
        CHANNEL_ID
    )

    if channel is None:

        try:

            channel = await bot.fetch_channel(
                CHANNEL_ID
            )

        except Exception as error:

            print(
                f"ERROR finding channel: {error}"
            )

            return

    # --------------------------------------------------------
    # Get user
    # --------------------------------------------------------

    try:

        user = await bot.fetch_user(
            REMINDER_USER_ID
        )

    except Exception as error:

        print(
            f"ERROR finding reminder user: {error}"
        )

        return

    # --------------------------------------------------------
    # Reminder
    # --------------------------------------------------------

    message = (
        f"{user.mention}\n\n"
        "🔔 **EVENT REMINDER** 🔔\n\n"
        "Please check today's Alliance Event "
        "and this week's LSM.\n\n"
        "🚨 **Alliance Event**\n"
        "Daily deployment information.\n\n"
        "🌪️ **LSM**\n"
        "Weekly LSM information.\n\n"
        "👇 Select an option below."
    )

    # --------------------------------------------------------
    # Send
    # --------------------------------------------------------

    await channel.send(
        message,
        view=EventView()
    )

    print(
        f"Reminder sent: "
        f"{get_now().strftime('%d/%m/%Y %H:%M:%S')}"
    )


# ============================================================
# DAILY TIMER
# ============================================================

@tasks.loop(minutes=1)
async def reminder_loop():

    now = get_now()

    if (
        now.hour == REMINDER_HOUR
        and
        now.minute == REMINDER_MINUTE
    ):

        await send_daily_reminder()


# ============================================================
# PANEL COMMAND
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def panel(ctx):

    await ctx.send(
        "🎛️ **Event Control Panel**\n\n"
        "Choose an event:",
        view=EventView()
    )


# ============================================================
# TEST COMMAND
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def test(ctx):

    await ctx.send(
        "🧪 **Testing Event Panel**",
        view=EventView()
    )


# ============================================================
# ALLIANCE COMMAND
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def alliance(ctx):

    await ctx.send(
        make_alliance_event()
    )


# ============================================================
# LSM COMMAND
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def lsm(ctx):

    await ctx.send(
        make_lsm_event()
    )


# ============================================================
# BOT READY
# ============================================================

@bot.event
async def on_ready():

    print(
        "========================================"
    )

    print(
        f"Logged in as: {bot.user}"
    )

    print(
        f"UK Time: "
        f"{get_now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # Make buttons work after restart
    # --------------------------------------------------------

    bot.add_view(
        EventView()
    )

    # --------------------------------------------------------
    # Start daily reminder
    # --------------------------------------------------------

    if not reminder_loop.is_running():

        reminder_loop.start()

        print(
            "Daily reminder system started."
        )


# ============================================================
# ERROR HANDLER
# ============================================================

@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        commands.MissingPermissions
    ):

        await ctx.send(
            "❌ You do not have permission "
            "to use this command.",
            delete_after=5
        )

        return

    print(
        f"Command error: {error}"
    )


# ============================================================
# START
# ============================================================

bot.run(TOKEN)
