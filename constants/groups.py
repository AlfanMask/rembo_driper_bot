from typing import Final
from constants import univs
from dotenv import load_dotenv
load_dotenv()
import os

# get group_chat_ids envs
group_chat_id_uns = os.getenv("GROUP_CHAT_ID_UNS")
group_chat_id_ums = os.getenv("GROUP_CHAT_ID_UMS")
group_chat_id_uny = os.getenv("GROUP_CHAT_ID_UNY")
group_chat_id_uns_wa_kampusku = os.getenv("GROUP_CHAT_ID_UNS_WA_KAMPUSKU") # added for fun group
group_chat_id_merlyn = os.getenv("GROUP_CHAT_ID_MERLYN") # added for fun group with merlyn

group_chat_ids: Final[dict] = {
    univs.uns: group_chat_id_uns,
    univs.ums: group_chat_id_ums,
    univs.uny: group_chat_id_uny,
    "uns_wa_kampusku": group_chat_id_uns_wa_kampusku, # added for fun group
    "group_chat_id_merlyn": group_chat_id_merlyn, # added for fun group with merlyn
}

# get group_chat_rembo_topic_ids envs
group_chat_id_play_rembo_uns = os.getenv("GROUP_CHAT_ID_PLAY_REMBO_UNS")
group_chat_id_play_rembo_ums = os.getenv("GROUP_CHAT_ID_PLAY_REMBO_UMS")
group_chat_id_play_rembo_uny = os.getenv("GROUP_CHAT_ID_PLAY_REMBO_UNY")

group_chat_play_rembo_ids: Final[dict] = {
    univs.uns: group_chat_id_play_rembo_uns,
    univs.ums: group_chat_id_play_rembo_ums,
    univs.uny: group_chat_id_play_rembo_uny,
}