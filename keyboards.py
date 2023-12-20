# keyboards for three languages: uz, ru, en
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="🇺🇿 O'zbekcha"),
        KeyboardButton(text="🇷🇺 Русский"),
        KeyboardButton(text="🇬🇧 English")
    ]
])

