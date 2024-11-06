import os
import sys
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

# aiogram lib
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# import modules
from constants import input_state, premium_type

# keyboard: for move univ of user
def set_move_univ_univ_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_move_univ_select}"),
        ],
        [
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_move_univ_select}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_move_univ_select}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_move_univ_select}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_move_univ_select}")],
    ])
    
    return keyboard

# keyboard: for move univ of user
def set_change_premtype_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=premium_type.PREMIUM.ANON, callback_data=f"{premium_type.PREMIUM.ANON}-{input_state.flag_change_premtype_select}"),
            InlineKeyboardButton(text=premium_type.PREMIUM.MENFESS, callback_data=f"{premium_type.PREMIUM.MENFESS}-{input_state.flag_change_premtype_select}"),
        ],
        [
            InlineKeyboardButton(text=premium_type.PREMIUM.DRIVER, callback_data=f"{premium_type.PREMIUM.DRIVER}-{input_state.flag_change_premtype_select}"),
            InlineKeyboardButton(text=premium_type.PREMIUM.BOTH, callback_data=f"{premium_type.PREMIUM.BOTH}-{input_state.flag_change_premtype_select}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_change_premtype_select}")],
    ])
    
    return keyboard

def set_move_univ_back_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=input_state.back[user_lang], callback_data=f"{input_state.back[user_lang]}-{input_state.flag_move_univ}")],
    ])
    
    return keyboard


# keyboard: checks
def set_check_online_24h(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_check_online_24h}"),
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_check_online_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_check_online_24h}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_check_online_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_move_univ_select}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_move_univ_select}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_move_univ_select}"),
        ],
        [
            InlineKeyboardButton(text=input_state.all, callback_data=f"{input_state.all}-{input_state.flag_check_online_24h}"),  
            InlineKeyboardButton(text=input_state.other_univs, callback_data=f"{input_state.other_univs}-{input_state.flag_check_online_24h}"),  
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_check_online_24h}")],
    ])
    
    return keyboard

def set_check_online_1h(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_check_online_1h}"),
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_check_online_1h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_check_online_1h}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_check_online_1h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_check_online_24h}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_check_online_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_check_online_24h}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_check_online_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.all, callback_data=f"{input_state.all}-{input_state.flag_check_online_1h}"),
            InlineKeyboardButton(text=input_state.other_univs, callback_data=f"{input_state.other_univs}-{input_state.flag_check_online_1h}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_check_online_1h}")],
    ])
    
    return keyboard

def set_check_online_1m(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_check_online_1m}"),
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_check_online_1m}"),
        ],
        [
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_check_online_1m}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_check_online_1m}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_check_online_1m}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_check_online_1m}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_check_online_1m}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_check_online_1m}"),
        ],
        [
            InlineKeyboardButton(text=input_state.all, callback_data=f"{input_state.all}-{input_state.flag_check_online_1m}"),
            InlineKeyboardButton(text=input_state.other_univs, callback_data=f"{input_state.other_univs}-{input_state.flag_check_online_1m}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_check_online_1m}")],
    ])
    
    return keyboard

def set_check_new_24h(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_check_new_24h}"),
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_check_new_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_check_new_24h}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_check_new_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_check_new_24h}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_check_new_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_check_new_24h}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_check_new_24h}"),
        ],
        [
            InlineKeyboardButton(text=input_state.all, callback_data=f"{input_state.all}-{input_state.flag_check_new_24h}"),
            InlineKeyboardButton(text=input_state.other_univs, callback_data=f"{input_state.other_univs}-{input_state.flag_check_new_24h}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_check_new_24h}")],
    ])
    
    return keyboard

def set_check_all_users(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=input_state.uns, callback_data=f"{input_state.uns}-{input_state.flag_check_all_users}"),
            InlineKeyboardButton(text=input_state.ugm, callback_data=f"{input_state.ugm}-{input_state.flag_check_all_users}"),
        ],
        [
            InlineKeyboardButton(text=input_state.undip, callback_data=f"{input_state.undip}-{input_state.flag_check_all_users}"),
            InlineKeyboardButton(text=input_state.unnes, callback_data=f"{input_state.unnes}-{input_state.flag_check_all_users}"),
        ],
        [
            InlineKeyboardButton(text=input_state.unpad, callback_data=f"{input_state.unpad}-{input_state.flag_check_all_users}"),
            InlineKeyboardButton(text=input_state.ui, callback_data=f"{input_state.ui}-{input_state.flag_check_all_users}"),
        ],
        [
            InlineKeyboardButton(text=input_state.uny, callback_data=f"{input_state.uny}-{input_state.flag_check_all_users}"),
            InlineKeyboardButton(text=input_state.itb, callback_data=f"{input_state.itb}-{input_state.flag_check_all_users}"),
        ],
        [
            InlineKeyboardButton(text=input_state.all, callback_data=f"{input_state.all}-{input_state.flag_check_all_users}"),
            InlineKeyboardButton(text=input_state.other_univs, callback_data=f"{input_state.other_univs}-{input_state.flag_check_all_users}"),
        ],
        [InlineKeyboardButton(text=input_state.close[user_lang], callback_data=f"{input_state.close[user_lang]}-{input_state.flag_check_all_users}")],
    ])
    
    return keyboard

# keyboard: for clean up
def set_close_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    return keyboard