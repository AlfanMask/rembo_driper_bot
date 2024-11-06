import os
import sys

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

from typing import Final
from constants import lang, premium_type

#univs
uns: Final[str] = "UNS"
undip: Final[str] = "UNDIP"
ugm: Final[str] = "UGM"
unnes: Final[str] = "UNNES"
unpad: Final[str] = "UNPAD"
ui: Final[str] = "UI"
uny: Final[str] = "UNY"
itb: Final[str] = "ITB"
all: Final[str] = "ALL"
listed_univs: Final[list] = [uns, undip, ugm, unnes, unpad, ui, uny, itb]
other_univs: Final[str] = "OTHER UNIVS"
has_shop_univs: Final[list] = [uns, unpad]

# only admin
banned_user: Final[str] = "Banned user by id"
unbanned_user: Final[str] = "Unbanned user by id"
register_driver: Final[str] = "Register driver"
unregister_driver: Final[str] = "Unregister driver"
set_premium: Final[str] = "Set premium user by id in (x) weeks"
set_bid_quota: Final[str] = "Set premium user by id in (x) bid quota"
set_ntwb: Final[str] = "Set Num Typed Banned Words user by id"
check_referrals: Final[str] = "Check number of shared referrals by user id"
reset_special_quota: Final[str] = "Reset special quota by user id"
reset_mager_quota: Final[str] = "Reset mager quota by user id"
delete_input_state: Final[str] = "Delete input state by user id"
delete_room: Final[str] = "Delete user room by user id"
custom_query: Final[str] = "Custom QUERY"
broadcast: Final[str] = "Broadcast message"

# buttons
back: Final[dict] = { lang.en: "⬅️ back", lang.id: "⬅️ kembali", lang.jw: "⬅️ mbalek" }
close: Final[dict] = { lang.en: "❌ Close", lang.id: "❌ Tutup", lang.jw: "❌ Tutup" }

# flags
flag_move_univ_select: Final[str] = "flag_move_univ_select"
flag_change_premtype_select: Final[str] = "flag_change_premtype_select"
flag_move_univ: Final[str] = "flag_move_univ"
flag_check_online_24h: Final[str] = "flag_check_online_24h"
flag_check_online_1h: Final[str] = "flag_check_online_1h"
flag_check_online_1m: Final[str] = "flag_check_online_1m"
flag_check_new_24h: Final[str] = "flag_check_new_24h"
flag_check_all_users: Final[str] = "flag_check_all_users"

move_univ: Final[dict[str]] = {
    uns: "🤖 Move to: UNS",
    undip: "🤖 Move to: UNDIP",
    ugm: "🤖 Move to: UGM",
    unnes: "🤖 Move to: UNNES",
    unpad: "🤖 Move to: UNPAD",
    ui: "🤖 Move to: UI",
    uny: "🤖 Move to: UNY",
    itb: "🤖 Move to: ITB",
}

change_premtype: Final[dict[str]] = {
    premium_type.PREMIUM.ANON: "🤖 Change premium type: ANON",
    premium_type.PREMIUM.MENFESS: "🤖 Change premium type: MENFESS",
    premium_type.PREMIUM.DRIVER: "🤖 Change premium type: DRIVER",
    premium_type.PREMIUM.BOTH: "🤖 Change premium type: BOTH",
}

error_input: Final[dict] = { lang.en: "❗ Error, please select the correct input", lang.id: "❗ Error, tolong masukkan input yang sesuai", lang.jw: "❗ Error, tulung lebokke input sing sesuai" }