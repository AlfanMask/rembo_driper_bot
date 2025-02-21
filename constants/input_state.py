import os
import sys

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

from typing import Final
from constants import lang, premium_type


# buttons
default: Final[dict] = { lang.en: "↻ Default", lang.id: "↻ Default", lang.jw: "↻ Default" }
back: Final[dict] = { lang.en: "⬅️ back", lang.id: "⬅️ kembali", lang.jw: "⬅️ mbalek" }
close: Final[dict] = { lang.en: "❌ Close", lang.id: "❌ Tutup", lang.jw: "❌ Tutup" }

# modes
chatting: Final[dict] = { lang.en: "💬 Chatting", lang.id: "💬 Chattingan", lang.jw: "💬 Chattingan" }
serious: Final[dict] = { lang.en: "📖 Serious", lang.id: "📖 Serius", lang.jw: "📖 Serius" }

# input_states
input_setting_ref_ai: Final[str] = "input_setting_ref_ai"

# flags
flag_setting_pref_ai: Final[str] = "flag_setting_pref_ai"
flag_setting_mode_ai: Final[str] = "flag_setting_mode_ai"

error_input: Final[dict] = { lang.en: "❗ Error, please select the correct input", lang.id: "❗ Error, tolong masukkan input yang sesuai", lang.jw: "❗ Error, tulung lebokke input sing sesuai" }