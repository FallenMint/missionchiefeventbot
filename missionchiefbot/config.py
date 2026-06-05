import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# REQUIRED SETTINGS
# -----------------------
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN in .env")

if not CHANNEL_ID:
    raise Exception("Missing CHANNEL_ID in .env")

CHANNEL_ID = int(CHANNEL_ID)


# -----------------------
# CONTENT DATA
# -----------------------

UK_LOCATIONS = [
    "London",
    "Birmingham",
    "Manchester",
    "Liverpool",
    "Leeds",
    "Sheffield",
    "Bristol",
    "Nottingham",
    "Newcastle",
    "Glasgow",
    "Cardiff",
    "Belfast",
]

EVENTS = [
    "Storm",
    "Section 60",
    "Pandemic",
    "Autumn Weather",
    "Spring Weather",
    "Summer Weather",
    "Sport Weather",
]

UNITS = [
    "Fire Engines",
    "Aerial Appliance Trucks",
    "Fire Officers",
    "Ambulance Control Units",
    "BSU",
    "Hazmat",
    "Rescue Support",
    "Foam Unit",
    "Police Cars",
    "Armed Response",
    "DSU",
    "Traffic Cars",
    "Police Helicopters",
    "OTL",
    "PRV",
    "SRV",
    "Welfare",
    "ATV",
    "Mass Casualty Equipment",
    "Ambulance Officers",
]

RULES_TEXT = """
Possible Prisoners: Up to 100
Possible Patients: Up to 100
Transport Probability: 80%
Hospital Department: General Internal
Critical Care Quote: 0
"""
