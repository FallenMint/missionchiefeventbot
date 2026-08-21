import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# DISCORD SETTINGS
# ============================================================

TOKEN = os.getenv(
    "DISCORD_TOKEN"
)

CHANNEL_ID = os.getenv(
    "CHANNEL_ID"
)

REMINDER_USER_ID = os.getenv(
    "REMINDER_USER_ID"
)


if not TOKEN:
    raise Exception(
        "Missing DISCORD_TOKEN in .env"
    )


if not CHANNEL_ID:
    raise Exception(
        "Missing CHANNEL_ID in .env"
    )


if not REMINDER_USER_ID:
    raise Exception(
        "Missing REMINDER_USER_ID in .env"
    )


CHANNEL_ID = int(
    CHANNEL_ID
)

REMINDER_USER_ID = int(
    REMINDER_USER_ID
)


# ============================================================
# TIME SETTINGS
# ============================================================

TIMEZONE = "Europe/London"

REMINDER_HOUR = 12

REMINDER_MINUTE = 0
