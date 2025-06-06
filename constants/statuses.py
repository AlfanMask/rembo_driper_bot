from typing import Final
from constants import lang, ai_assistant_default_preference_character, ai_assistant_mode

# default
def start_information() -> str:
    return """
Haloo, Rembo di sini kukuruyuukk...

Rembo punya fitur:
/mode: untuk mengganti mode AI
/karakter: untuk menambahkan karakter AI kamu sendiri
/reset: untuk reset memori AI dan ngobrol dari awal lagi

Selamat chattingan dengan rembo 😊
"""

# setting character
def msg_setting_character(active_preference: str) -> str:
    return f"""
<b>» Karakter AI Rembo saati ini: {active_preference}</b>

Untuk mengganti prerefensi karakter, silakan ketikkan di bawah ini (misal: sensian dan pemarah):
"""
msg_cancel_setting_character: Final[str] = "Kamu telah membatalkan perubahan karakter AI"
msg_default_setting_character: Final[str] = f"» Setting karakter AI dikembalikan ke default: <b>{ai_assistant_default_preference_character.default}</b>"
def msg_success_setting_character(active_preference: str) -> str:
    return f"» Karakter AI Rembo telah diubah menjadi: <b>{active_preference}</b>"

# setting mode
def msg_setting_mode() -> str:
    return f"""
<b>» Setting Mode Rembo</b>

• <b>Mode Chattingan</b>
  1) Alay. untuk rembo yang suka dengerin curhatan, cerita, hingga chat absurdmu.
  2) Biasa. rembo jadi temen lama kamu, bisa kamu ajak chattingan kek manusia normal.
  
• <b>Mode Serius</b> untuk rembo yang pintar, yang bisa nemenin kamu belajar, dan ngasih jawaban apapun soal pertanyaanmu (kek AI pada umumnya)
"""

# reset
msg_success_reset_memory: Final[str] = "» Memori Rembo telah berhasil dihapuskan, selamat chat lagi dari 0 😊"

# AI
error_ai_busy: Final[str] = f"<i>Aduhh, aku lagi cape. Aku jawab ntaran yaa, mau istirahat dulu 😴</i>"

# bot tasks
kick_drivers_inactive_start: str = "Okee bos, saya cek dulu siapa yang ga aktif dalam 3 bulan terakhir, nanti saya kick satu-satu 😊🙏"
kick_drivers_inactive_end: str = "Udahh selesai bos, bisa dicek jumlah member di grup ini sudah berkurang 🙏"