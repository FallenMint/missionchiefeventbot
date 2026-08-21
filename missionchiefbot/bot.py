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
# FILE SETTINGS
# ============================================================

EVENT_FILE = "events.json"


# ============================================================
# TIME FUNCTIONS
# ============================================================

def get_now():
    return datetime.now(
        ZoneInfo(TIMEZONE)
    )


def get_today():
    return get_now().strftime(
        "%Y-%m-%d"
    )


def get_display_date():
    return get_now().strftime(
        "%d/%m/%Y"
    )


def get_week():
    return get_now().strftime(
        "%Y-W%U"
    )


# ============================================================
# LOAD EVENT DATA
# ============================================================

def load_events():

    if not os.path.exists(EVENT_FILE):

        print(
            "ERROR: events.json does not exist."
        )

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
    # Find today's Alliance event
    # --------------------------------------------------------

    event = alliance.get(
        today
    )

    # --------------------------------------------------------
    # If there isn't a specific event for today,
    # use the default event.
    # --------------------------------------------------------

    if event is None:

        event = alliance.get(
            "default"
        )

    # --------------------------------------------------------
    # No event found
    # --------------------------------------------------------

    if event is None:

        return (
            "🚨 **ALLIANCE EVENT** 🚨\n\n"
            f"📅 **Date:** {get_display_date()}\n\n"
            "❌ There is no Alliance Event configured "
            "for today."
        )

    # --------------------------------------------------------
    # Basic event information
    # --------------------------------------------------------

    event_name = event.get(
        "name",
        "Alliance Event"
    )

    location = event.get(
        "location",
        "Not specified"
    )

    people = event.get(
        "people",
        []
    )

    message = (
        "🚨 **ALLIANCE EVENT** 🚨\n\n"
        f"📛 **Event Name:** {event_name}\n"
        f"📅 **Date:** {get_display_date()}\n"
        f"📍 **Location:** {location}\n\n"
        "👥 **PEOPLE TO SEND:**\n"
    )

    # --------------------------------------------------------
    # People
    # --------------------------------------------------------

    if not people:

        message += (
            "No people have been configured.\n"
        )

    else:

        for person in people:

            person_name = person.get(
                "name",
                "Unknown"
            )

            person_location = person.get(
                "location",
                location
            )

            message += (
                f"• **{person_name}** → {person_location}\n"
            )

    # --------------------------------------------------------
    # Optional instructions
    # --------------------------------------------------------

    instructions = event.get(
        "instructions",
        ""
    )

    if instructions:

        message += (
            "\n📝 **Instructions:**\n"
            f"{instructions}\n"
        )

    message += (
        "\n━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Today's Alliance information."
    )

    return message


# ============================================================
# LSM EVENT
# ============================================================

def make_lsm_event():

    data = load_events()

    lsm = data.get(
        "lsm",
        {}
    )

    current_week = get_week()

    # --------------------------------------------------------
    # Find this week's LSM
    # --------------------------------------------------------

    event = lsm.get(
        current_week
    )

    # --------------------------------------------------------
    # If there isn't a specific week,
    # use the default.
    # --------------------------------------------------------

    if event is None:

        event = lsm.get(
            "default"
        )

    # --------------------------------------------------------
    # No LSM found
    # --------------------------------------------------------

    if event is None:

        return (
            "🌪️ **LSM EVENT** 🌪️\n\n"
            f"📅 **Week:** {current_week}\n\n"
            "❌ No LSM has been configured "
            "for this week."
        )

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    event_type = event.get(
        "type",
        "LSM"
    )

    event_name = event.get(
        "name",
        "LSM Event"
    )

    missions = event.get(
        "missions",
        []
    )

    message = (
        "🌪️ **LSM EVENT** 🌪️\n\n"
        f"📛 **Event Name:** {event_name}\n"
        f"📋 **Type:** {event_type}\n"
        f"📅 **Week:** {current_week}\n\n"
        "🎯 **MISSIONS:**\n"
    )

    # --------------------------------------------------------
    # Missions
    # --------------------------------------------------------

    if not missions:

        message += (
            "No missions have been configured.\n"
        )

    else:

        for number, mission in enumerate(
            missions,
            start=1
        ):

            mission_name = mission.get(
                "name",
                "Unknown Mission"
            )

            location = mission.get(
                "location",
                "Not specified"
            )

            message += (
                f"\n**{number}. {mission_name}**\n"
                f"📍 **Location:** {location}\n"
            )

            # Optional mission instructions

            instructions = mission.get(
                "instructions",
                ""
            )

            if instructions:

                message += (
                    f"📝 {instructions}\n"
                )

    message += (
        "\n━━━━━━━━━━━━━━━━━━━━\n"
        "✅ This week's LSM information."
    )

    return message


# ============================================================
# BUTTON VIEW
# ============================================================

class EventView(discord.ui.View):

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
    # Create reminder
    # --------------------------------------------------------

    message = (
        f"{user.mention}\n\n"
        "🔔 **EVENT REMINDER** 🔔\n\n"
        "It's time to check today's events.\n\n"
        "🚨 **Alliance Event**\n"
        "Check today's Alliance deployment.\n\n"
        "🌪️ **LSM**\n"
        "Check this week's LSM missions.\n\n"
        "👇 **Choose the event you need below.**"
    )

    # --------------------------------------------------------
    # Send reminder
    # --------------------------------------------------------

    await channel.send(
        message,
        view=EventView()
    )

    print(
        f"Daily reminder sent at "
        f"{get_now().strftime('%d/%m/%Y %H:%M:%S')}"
    )


# ============================================================
# REMINDER LOOP
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
# ADMIN COMMAND - PANEL
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def panel(ctx):

    await ctx.send(
        "🎛️ **Event Control Panel**\n\n"
        "Choose an event below:",
        view=EventView()
    )


# ============================================================
# ADMIN COMMAND - TEST
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
# ADMIN COMMAND - ALLIANCE
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
# ADMIN COMMAND - LSM
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
    # Register persistent buttons
    # --------------------------------------------------------

    bot.add_view(
        EventView()
    )

    # --------------------------------------------------------
    # Start reminder system
    # --------------------------------------------------------

    if not reminder_loop.is_running():

        reminder_loop.start()

        print(
            "Daily reminder system started."
        )


# ============================================================
# COMMAND ERROR HANDLER
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
# START BOT
# ============================================================

bot.run(TOKEN)
