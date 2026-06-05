import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
from dotenv import load_dotenv

from config import TOKEN, CHANNEL_ID, UK_LOCATIONS, UNITS, EVENTS, RULES

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()


# -----------------------------
# SCENARIO SYSTEM (REALISM CORE)
# -----------------------------

SCENARIOS = [
    "Multi-vehicle motorway collision with fire involvement",
    "High-rise residential fire with entrapments",
    "Gas main explosion in urban commercial district",
    "Large stadium crowd disorder and medical incidents",
    "Chemical plant leak with hazardous atmosphere",
    "Severe flooding with multiple stranded casualties",
    "Armed police response to active threat incident",
    "Mass casualty train derailment",
    "Warehouse fire with structural collapse risk",
    "Public disorder following major event escalation",
    "Storm damage leading to widespread emergency calls",
    "Suspicious package / controlled evacuation scenario",
    "Industrial accident involving heavy machinery failure"
]


# -----------------------------
# GENERATORS
# -----------------------------

def generate_mission():
    return {
        "name": random.choice(SCENARIOS),
        "location": random.choice(UK_LOCATIONS),
        "units": random.sample(UNITS, k=10)
    }


def generate_event():
    event_type = random.choice(EVENTS)

    return {
        "name": f"{event_type} Major Incident",
        "location": random.choice(UK_LOCATIONS),
        "event_type": event_type,
        "units": random.sample(UNITS, k=12)
    }


# -----------------------------
# MESSAGE FORMATTER
# -----------------------------

def format_mission(m):
    return (
        f"🚨 **LARGE SCALE MISSION** 🚨\n\n"
        f"📛 Scenario: {m['name']}\n"
        f"📍 Location: {m['location']}\n\n"
        f"🚒 Units Required:\n" +
        "\n".join(f"- {u}" for u in m['units']) +
        "\n\n"
        f"📊 Rules:\n"
        f"- Patients: Up to 100\n"
        f"- Prisoners: Up to 100\n"
        f"- Transport Probability: 80%\n"
        f"- Hospital Dept: General Internal\n"
        f"- Critical Care Quote: 0"
    )


def format_event(e):
    return (
        f"🌍 **WEEKLY MAJOR EVENT** 🌍\n\n"
        f"📛 Event: {e['name']}\n"
        f"📍 Location: {e['location']}\n\n"
        f"📦 Type: {e['event_type']}\n"
        f"🟦 Area: Large Rectangular Operational Zone\n"
        f"⏱ Call Volume: 30 seconds\n\n"
        f"🚨 Units Required:\n" +
        "\n".join(f"- {u}" for u in e['units'])
    )


# -----------------------------
# DISCORD COMMANDS (TESTING)
# -----------------------------

@bot.command()
async def test(ctx):
    m = generate_mission()
    await ctx.send(format_mission(m))


@bot.command()
async def testevent(ctx):
    e = generate_event()
    await ctx.send(format_event(e))


# -----------------------------
# SCHEDULER
# -----------------------------

async def post_daily():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(format_mission(generate_mission()))


async def post_weekly():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(format_event(generate_event()))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    scheduler.add_job(post_daily, "cron", hour=9, minute=0)
    scheduler.add_job(post_weekly, "cron", day_of_week="sun", hour=18, minute=0)

    scheduler.start()


# -----------------------------
# RUN
# -----------------------------

bot.run(TOKEN)
