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
# FILES
# ============================================================

EVENT_FILE = "events.json"


# ============================================================
# LOAD EVENTS
# ============================================================

def load_events():

    if not os.path.exists(EVENT_FILE):

        print("events.json not found!")

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
            f"Failed to load events.json: {error}"
        )

        return {
            "alliance": {},
            "lsm": {}
        }


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


def get_display_date():

    return get_now().strftime(
        "%d/%m/%Y"
    )


def get_week():

    return get_now().strftime(
        "%Y-W%U"
    )


# ============================================================
# ALLIANCE EVENT
# ============================================================

def make_alliance_event():

    data = load_events()

    today = get_today()

    alliance_events = data.get(
        "alliance",
        {}
    )

    # --------------------------------------------------------
    # Look for today's event
    # --------------------------------------------------------

    event = alliance_events.get(
        today
    )

    # --------------------------------------------------------
    # If there isn't a specific event for today,
    # use the default event
    # --------------------------------------------------------

    if event is None:

        event = alliance_events.get(
            "default"
        )

    # --------------------------------------------------------
    # No event configured
    # --------------------------------------------------------

    if event is None:

        return (
            "🚨 **ALLIANCE EVENT** 🚨\n\n"
            f"📅 **Date:** {get_display_date()}\n\n"
            "❌ No Alliance Event has been configured "
            "for today."
        )

    # --------------------------------------------------------
    # Event information
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
        f"📛 **Event:** {event_name}\n"
        f"📅 **Date:** {get_display_date()}\n"
        f"📍 **Location:** {location}\n\n"
        "👥 **SEND:**\n"
    )

    # --------------------------------------------------------
    # People / units
    # --------------------------------------------------------

    if not people:

        message += (
            "No people or units have been specified.\n"
        )

    else:

        for person in people:

            name = person.get(
                "name",
                "Unknown"
            )

            send_location = person.get(
                "location",
                location
            )

            message += (
                f"• **{name}** → {send_location}\n"
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
        "✅ Alliance Event information loaded."
    )

    return message


# ============================================================
# LSM EVENT
# ============================================================

def make_lsm_event():

    data = load_events()

    current_week = get_week()

    lsm_data = data.get(
        "lsm",
        {}
    )

    # --------------------------------------------------------
    # Look for current week
    # --------------------------------------------------------

    event = lsm_data.get(
        current_week
    )

    # --------------------------------------------------------
    # If no current week is configured,
    # use default
    # --------------------------------------------------------

    if event is None:

        event = lsm_data.get(
            "default"
        )

    # --------------------------------------------------------
    # No LSM configured
    # --------------------------------------------------------

    if event is None:

        return (
            "🌪️ **LSM EVENT** 🌪️\n\n"
            f"📅 **Week:** {current_week}\n\n"
            "❌ No LSM information has been configured "
            "for this week."
        )

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

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
        f"📛 **Event:** {event_name}\n"
        f"📅 **Week:** {current_week}\n\n"
        "📋 **MISSIONS:**\n"
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

            # -----------------------------------------------
            # Optional people / units
            # -----------------------------------------------

            people = mission.get(
                "people",
                []
            )

            if people:

                message += (
                    "👥 **Send:**\n"
                )

                for person in people:

                    message += (
                        f"• {person}\n"
                    )

            # -----------------------------------------------
            # Optional instructions
            # -----------------------------------------------

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
        "✅ LSM information loaded."
    )

    return message


# ============================================================
# EVENT BUTTONS
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
# SEND DAILY REMINDER
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
                f"Could not find channel: {error}"
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
            f"Could not find reminder user: {error}"
        )

        return

    # --------------------------------------------------------
    # Reminder message
    # --------------------------------------------------------

    message = (
        f"{user.mention}\n\n"
        "🔔 **DAILY EVENT REMINDER** 🔔\n\n"
        "Please check the event information for today.\n\n"
        "🚨 **Alliance Event**\n"
        "Check today's Alliance deployment.\n\n"
        "🌪️ **LSM**\n"
        "Check this week's LSM missions.\n\n"
        "👇 Select the event you need below."
    )

    # --------------------------------------------------------
    # Send message
    # --------------------------------------------------------

    await channel.send(
        message,
        view=EventView()
    )

    print(
        "Daily event reminder sent."
    )


# ============================================================
# DAILY REMINDER LOOP
# ============================================================

@tasks.loop(minutes=1)
async def reminder_loop():

    now = get_now()

    # --------------------------------------------------------
    # Check if it is exactly 12:00
    # --------------------------------------------------------

    if (
        now.hour == REMINDER_HOUR
        and
        now.minute == REMINDER_MINUTE
    ):

        await send_daily_reminder()


# ============================================================
# COMMAND - PANEL
# ============================================================

@bot.command()
@commands.has_permissions(
    administrator=True
)
async def panel(ctx):

    await ctx.send(
        "🎛️ **Event Control Panel**",
        view=EventView()
    )


# ============================================================
# COMMAND - TEST
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
# COMMAND - ALLIANCE
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
# COMMAND - LSM
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
        "================================="
    )

    print(
        f"Logged in as: {bot.user}"
    )

    print(
        f"UK Time: {get_now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    print(
        "================================="
    )

    # --------------------------------------------------------
    # Keep buttons working after restart
    # --------------------------------------------------------

    bot.add_view(
        EventView()
    )

    # --------------------------------------------------------
    # Start reminder loop
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
            "❌ You do not have permission to use this command.",
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
