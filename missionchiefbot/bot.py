import discord
from discord.ext import commands, tasks
import random
import json
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1515313354992914469

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

UK_TZ = pytz.timezone("Europe/London")

UK_LOCATIONS = ["London","Birmingham","Manchester","Liverpool","Leeds","Sheffield","Bristol","Nottingham","Newcastle","Glasgow","Cardiff","Belfast"]

EVENTS = ["Section 60","Pandemic","Autumn Weather","Spring Weather","Summer Weather","Sport Weather"]

LSM_TYPES = ["Mass Casualty Response","Large Scale Fire Incident","Multi-Vehicle Pileup","Citywide Emergency","Major Infrastructure Failure"]

SCENARIOS = ["Motorway Collision","High Rise Fire","Chemical Leak","Train Derailment","Stadium Incident","Warehouse Fire","Flood Rescue","Aircraft Crash"]

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_daily":"", "last_weekly":0}
    with open(STATE_FILE,"r") as f:
        return json.load(f)

def save_state(s):
    with open(STATE_FILE,"w") as f:
        json.dump(s,f,indent=4)

def channel():
    return bot.get_channel(CHANNEL_ID)

def alliance_event():
    return f"""🚨 ALLIANCE EVENT 🚨

Scenario: {random.choice(SCENARIOS)}
Location: {random.choice(UK_LOCATIONS)}
"""

def lsm_event():
    return f"""🌪️ LSM EVENT 🌪️

Type: {random.choice(LSM_TYPES)}
Location: {random.choice(UK_LOCATIONS)}
"""

class EventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Alliance Event", style=discord.ButtonStyle.green, custom_id="a")
    async def a(self, interaction, button):
        await interaction.response.send_message(alliance_event(), ephemeral=True)

    @discord.ui.button(label="LSM Event", style=discord.ButtonStyle.red, custom_id="b")
    async def b(self, interaction, button):
        await interaction.response.send_message(lsm_event(), ephemeral=True)

@tasks.loop(minutes=1)
async def daily():
    now = datetime.now(UK_TZ)
    s = load_state()
    today = now.strftime("%Y-%m-%d")

    if now.hour == 12 and now.minute == 0:
        if s["last_daily"] != today:
            ch = channel()
            if ch:
                await ch.send(alliance_event(), view=EventView())
            s["last_daily"] = today
            save_state(s)

@tasks.loop(minutes=5)
async def weekly():
    s = load_state()
    now = datetime.now(UK_TZ).timestamp()

    if now - s["last_weekly"] > 604800:
        ch = channel()
        if ch:
            await ch.send(lsm_event(), view=EventView())
        s["last_weekly"] = now
        save_state(s)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(EventView())
    daily.start()
    weekly.start()

@bot.command()
async def alliance(ctx):
    await ctx.send(alliance_event(), view=EventView())

@bot.command()
async def lsm(ctx):
    await ctx.send(lsm_event(), view=EventView())

bot.run(TOKEN)
EOF
