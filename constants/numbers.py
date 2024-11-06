import os
import sys
from typing import Final
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

# numbers
num_of_min_referral: Final[int] = 5
num_of_weeks_added: Final[int] = 1
num_default_special_quota: Final[int] = 15 # WEEKLY QUOTA
num_default_mager_quota: Final[int] = 3
min_mager_perweek_to_prem: int = 10
min_comment_points_perweek_to_prem: int = 100
week_of_prem_reward_mager_and_comment_reached: int = 1
num_default_bid_quota: int = 7
num_quota_bid_for_new_drivers: int = 250
num_quota_bid_premium_each_week: int = 250