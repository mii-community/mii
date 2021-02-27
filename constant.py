import os

import dotenv

dotenv.load_dotenv()

# token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

GUILD_ID = int(os.getenv("GUILD_ID", "608634154019586059"))
# channel
CH_DEBUG = int(os.getenv("CH_DEBUG", "815174814222254090"))
CH_REGISTER = int(os.getenv("CH_REGISTER", "608656664601690142"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_ROOM_ARCHIVE", "711058666387800135"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))
CH_TWEET = int(os.getenv("CH_TWEET", "744439125880602645"))
CH_MAIN = int(os.getenv("CH_MAIN", "608657253725372429"))

VOICE_CHANNELS = {
    "655319117691355166": {
        "vc_text": 655319030428598303,
        "name": "vc1",
    },
    "803798670029488180": {
        "vc_text": 803798580707459113,
        "name": "vc2",
    },
}
CH_AFK = int(os.getenv("CH_AFK", "655262798447902798"))
CH_PIN_STOCK = int(os.getenv("CH_PIN_STOCK", "807894608721084477"))
CH_TWITCH = int(os.getenv("CH_TWITCH", "814297105560109067"))

# role
ROLE_MEMBER = int(os.getenv("ROLE_MEMBER", "652885488197435422"))
ROLE_ARCHIVE = int(os.getenv("ROLE_ARCHIVE", "702420267309203466"))
ROLE_STREAMING = int(os.getenv("ROLE_STREAMING", "815320056556027924"))
# database
DATABASE_URL = os.getenv("DATABASE_URL")
TABLE_NAME = os.getenv("TABLE_NAME", "mii_channels")
COUNT_EMOJI = os.getenv("COUNT_EMOJI", "mii_count_custom_emoji")

# emoji
PIN_EMOJI = "\N{PUSHPIN}"
