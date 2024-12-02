# Задача "Витамины для всех!":
# Подготовка:
# Подготовьте Telegram-бота из последнего домашнего задания 13 модуля сохранив код с ним в файл module_14_3.py.
# Если вы не решали новые задания из предыдущего модуля рекомендуется выполнить их.
#
# Дополните ранее написанный код для Telegram-бота:
# Создайте и дополните клавиатуры:
# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"
# Создайте хэндлеры и функции к ним:
# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
# Функция get_buying_list должна выводить надписи 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
# Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging

logging.basicConfig(level= logging.INFO)
api = ''
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text= 'Информация')
button2 = KeyboardButton(text= 'Рассчитать')
button5 = KeyboardButton(text= 'Купить')
kb.add(button, button2)
kb.add(button5)

kb2 =  InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data= 'calories')
button4 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= 'Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ], resize_keyboard=True
)
kb2.add(button3, button4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands= ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'{i}.JPG', 'rb') as img:
            await message.answer_photo(img)
        await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb2)

@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) - 161')
    await call.answer()

@dp.message_handler(text= 'Информация')
async def info(message):
    await message.answer('Информация')

@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight= int(message.text))
    data = await state.get_data()
    await message.answer(f'Расчет калорийности по формуле Миффлина-Сан Жеора:'
                         f'\n1) для женщин: {10 * data["weight"] +6.25 * data["growth"] - 5 * data["age"] - 161} калорий '
                         f'\n2) для мужчин: {10 * data["weight"] +6.25 * data["growth"] - 5 * data["age"] + 5} калорий'
                         )
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)