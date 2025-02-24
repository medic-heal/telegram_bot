from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# from app.database.requests import get_catigories, get_category_item
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/register')],
    [KeyboardButton(text='/enter_scores')],
    [KeyboardButton(text='/view_scores')],
    
], resize_keyboard=True)