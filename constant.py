import os

import dotenv

dotenv.load_dotenv()

# token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# channel
CH_REGISTER = int(os.getenv("CH_REGISTER", "608656664601690142"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CH_VOICE = int(os.getenv("CH_VOICE", "655319117691355166"))
CH_VOICE_TEXT = int(os.getenv("CH_VOICE_TEXT", "655319030428598303"))
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_ROOM_ARCHIVE", "711058666387800135"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))

# role
ROLE_MEMBER = int(os.getenv("ROLE_MEMBER", "652885488197435422"))
ROLE_ARCHIVE = int(os.getenv("ROLE_ARCHIVE", "702420267309203466"))

# database
DATABASE_URL = os.getenv("DATABASE_URL")

# name
WEBHOOK_NAME = "mii"

# emoji
PIN_EMOJI = "\N{PUSHPIN}"
HIRAGANA_EMOJI = {
    "あ": "99_aa",
    "い": "98_ii",
    "う": "97_uu",
    "え": "96_ee",
    "お": "95_oo",
    "か": "94_ka",
    "き": "93_ki",
    "く": "92_ku",
    "け": "91_ke",
    "こ": "90_ko",
    "さ": "89_sa",
    "し": "88_si",
    "す": "87_su",
    "せ": "86_se",
    "そ": "85_so",
    "た": "84_ta",
    "ち": "83_ti",
    "つ": "82_tu",
    "て": "81_te",
    "と": "80_to",
    "な": "79_na",
    "に": "78_ni",
    "ぬ": "77_nu",
    "ね": "76_ne",
    "の": "75_no",
    "は": "74_ha",
    "ひ": "73_hi",
    "ふ": "72_hu",
    "へ": "71_he",
    "ほ": "70_ho",
    "ま": "69_ma",
    "み": "68_mi",
    "む": "67_mu",
    "め": "66_me",
    "も": "65_mo",
    "や": "64_ya",
    "ゆ": "63_yu",
    "よ": "62_yo",
    "ら": "61_ra",
    "り": "60_ri",
    "る": "59_ru",
    "れ": "58_re",
    "ろ": "57_ro",
    "わ": "56_wa",
    "を": "55_wo",
    "ん": "54_nn",
    "ぁ": "53_la",
    "ぃ": "52_li",
    "ぅ": "51_lu",
    "ぇ": "50_le",
    "ぉ": "49_lo",
    "っ": "48_ltu",
    "ゃ": "47_lya",
    "ゅ": "46_lyu",
    "ょ": "45_lyo",
    "〜": "44_nobasi",
    "ー": "44_nobasi",
    "！": "43_exclamation",
    "!": "43_exclamation",
    "？": "42_question",
    "?": "42_question",
    "、": "41_touten",
    ",": "41_touten",
    "。": "40_kuten",
    ".": "40_kuten",
}
