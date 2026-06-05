import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# -----------------------------
# EVENTS (weekly rotation)
# -----------------------------
EVENTS = [
    "Storm",
    "Section 60",
    "Pandemic",
    "Autumn Weather",
    "Spring Weather",
    "Summer Weather",
    "Sport Weather"
]

# -----------------------------
# UK LOCATIONS
# -----------------------------
UK_LOCATIONS = [
    "London", "Manchester", "Birmingham", "Liverpool",
    "Leeds", "Bristol", "Glasgow", "Edinburgh",
    "Cardiff", "Newcastle", "Sheffield", "Nottingham",
    "Southampton", "Leicester", "Oxford", "Cambridge"
]

# -----------------------------
# LARGE SCALE UNITS
# -----------------------------
UNITS = [
    "Fire Engines",
    "Aerial Appliance Trucks",
    "Fire Officers",
    "Ambulance Control Units",
    "BSU",
    "Hazmat",
    "Rescue Support",
    "Foam",
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
    "Mass Casuality Equipment",
    "Ambulance Officers"
]

# -----------------------------
# CONSTANT RULES
# -----------------------------
RULES = {
    "Possible Prisoners": "Up to 100",
    "Possible Patients": "Up to 100",
    "Transport Probability": "Up to 80%",
    "Hosp Department": "General Internal",
    "Critical Care Quote": 0
}
