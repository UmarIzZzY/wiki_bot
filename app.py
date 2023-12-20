import logging
import wikipedia
import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from config import API_TOKEN
from keyboards import lang_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# database connection
con = psycopg2.connect(
    database="wikibot",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = con.cursor()


class SearchState(StatesGroup):
    search = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f'Welcome {message.from_user.full_name}', reply_markup=lang_keyboard)


@dp.message_handler(Text(equals=['🇺🇿 O\'zbekcha', '🇷🇺 Русский', '🇬🇧 English']))
async def set_language(message: types.Message):
    if message.text == '🇺🇿 O\'zbekcha':
        await message.answer('Til muvaffaqiyatli o\'zgartirildi!\n'
                             'Iltimos, qidiruv so\'zini kiriting: ')
        await SearchState.search.set()
    elif message.text == '🇷🇺 Русский':
        await message.answer('Язык успешно изменен!\n'
                             'Пожалуйста, введите слово поиска: ')
        await SearchState.search.set()
    elif message.text == '🇬🇧 English':
        await message.answer('Language changed successfully!\n'
                             'Please, enter search word: ')
        await SearchState.search.set()
    else:
        await message.answer('Please, choose language: ', reply_markup=lang_keyboard)


@dp.message_handler(state=SearchState.search)
async def search(message: types.Message, state: FSMContext):
    await state.update_data(search=message.text)
    user_search = message.text
    try:
        result = wikipedia.summary(user_search)
        await message.answer(result)
        await state.finish()
        # save search history to database
        cur.execute("INSERT INTO messages_info (user_id, question, answer) VALUES (%s, %s, %s)",
                    (message.from_user.id, user_search, result))
        con.commit()
    except Exception as e:
        await message.answer(f"Error: {e}")
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
