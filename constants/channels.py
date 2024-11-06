from typing import Final 
from constants import input_state

import os
import sys
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# all channels chat ids from different univiersites
channel_fess_chat_id: Final[dict[str]] = {
    input_state.uns: os.getenv("CHANNEL_FESS_UNS_CHAT_ID"),
    input_state.undip: os.getenv("CHANNEL_FESS_UNDIP_CHAT_ID"),
    input_state.ugm: os.getenv("CHANNEL_FESS_UGM_CHAT_ID"),
    input_state.unnes: os.getenv("CHANNEL_FESS_UNNES_CHAT_ID"),
    input_state.unpad: os.getenv("CHANNEL_FESS_UNPAD_CHAT_ID"),
    input_state.ui: os.getenv("CHANNEL_FESS_UI_CHAT_ID"),
    input_state.uny: os.getenv("CHANNEL_FESS_UNY_CHAT_ID"),
    input_state.itb: os.getenv("CHANNEL_FESS_ITB_CHAT_ID"),
    
}

channel_mager_chat_id: Final[dict[str]] = {
    input_state.uns: os.getenv("CHANNEL_MAGER_UNS_CHAT_ID"),
    input_state.undip: os.getenv("CHANNEL_MAGER_UNDIP_CHAT_ID"),
    input_state.ugm: os.getenv("CHANNEL_MAGER_UGM_CHAT_ID"),
    input_state.unnes: os.getenv("CHANNEL_MAGER_UNNES_CHAT_ID"),
    input_state.unpad: os.getenv("CHANNEL_MAGER_UNPAD_CHAT_ID"),
    input_state.ui: os.getenv("CHANNEL_MAGER_UI_CHAT_ID"),
    input_state.uny: os.getenv("CHANNEL_MAGER_UNY_CHAT_ID"),
    input_state.itb: os.getenv("CHANNEL_MAGER_ITB_CHAT_ID"),
}

channel_shop_chat_id: Final[dict[str]] = {
    input_state.uns: os.getenv("CHANNEL_SHOP_UNS_CHAT_ID"),
    input_state.unpad: os.getenv("CHANNEL_SHOP_UNPAD_CHAT_ID"),
}

channel_friends_chat_id: Final[dict[str]] = {
    input_state.uns: os.getenv("CHANNEL_FRIEND_UNS_CHAT_ID"),
    input_state.undip: os.getenv("CHANNEL_FRIEND_UNDIP_CHAT_ID"),
    input_state.ugm: os.getenv("CHANNEL_FRIEND_UGM_CHAT_ID"),
    input_state.unnes: os.getenv("CHANNEL_FRIEND_UNNES_CHAT_ID"),
    input_state.unpad: os.getenv("CHANNEL_FRIEND_UNPAD_CHAT_ID"),
    input_state.ui: os.getenv("CHANNEL_FRIEND_UI_CHAT_ID"),
    input_state.uny: os.getenv("CHANNEL_FRIEND_UNY_CHAT_ID"),
    input_state.itb: os.getenv("CHANNEL_FRIEND_ITB_CHAT_ID"),
}