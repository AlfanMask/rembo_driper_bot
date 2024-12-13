from typing import Final
from constants import univs
from dotenv import load_dotenv
load_dotenv()
import os

# get group_chat_ids envs
group_chat_id_uns = os.getenv("GROUP_CHAT_ID_UNS")
group_chat_id_ums = os.getenv("GROUP_CHAT_ID_UMS")

group_chat_ids: Final[dict] = {
    univs.uns: group_chat_id_uns,
    univs.ums: group_chat_id_ums
}