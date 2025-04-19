from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# from app.database.requests import get_catigories, get_category_item
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# Главное меню с тремя кнопками: регистрация, ввод баллов и просмотр баллов
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/register')],           # Кнопка регистрации
    [KeyboardButton(text='/enter_scores')],       # Кнопка ввода баллов
    [KeyboardButton(text='/view_scores')],        # Кнопка просмотра баллов
    
    ], resize_keyboard=True
)