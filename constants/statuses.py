from typing import Final
from constants import lang, ai_assistant_default_preference_character

# setting
def msg_setting_character(active_preference: str) -> str:
    return f"""
<b>» Karakter AI Rembo saati ini: {active_preference}</b>

Untuk mengganti prerefensi karakter, silakan ketikkan di bawah ini (misal: sensian dan pemarah):
"""
msg_cancel_setting: Final[str] = "Kamu telah membatalkan perubahan karakter AI"
msg_default_setting: Final[str] = f"» Setting perefencei AI dikembalikan ke default: <b>{ai_assistant_default_preference_character.default}</b>"
def msg_success_setting(active_preference: str) -> str:
    return f"» Karakter AI Rembo telah diubah menjadi: <b>{active_preference}</b>"