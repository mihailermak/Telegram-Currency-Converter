#Token: 6183220089:AAF92022c-KAO_EAAcF3_TnsEfg5IxX0Rug

import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

#Запрос к openexchangerates.org
url = "https://openexchangerates.org/api/latest.json?app_id=36011ff3ad1d4279a3dcd70b5c8ad104"
response = requests.get(url)
rates = response.json()["rates"]

#Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

#Создаем бота, хранилище и диспетчер
bot = Bot(token='6183220089:AAF92022c-KAO_EAAcF3_TnsEfg5IxX0Rug')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Список поддерживаемых валют
currencies = ('USD', 'EUR', 'RUB', 'GBP', 'AED', 'ANG', 'AMD',
               'AZN', 'BAM', 'BYN', 'CAD', 'CHF', 'CLP', 'CNY',
               'COP', 'CRC', 'CUP', 'CZK', 'DKK', 'EEK', 'EGP',
               'HKD', 'IDR', 'INR', 'IRR', 'ISK', 'JPY', 'KGS',
               'KRW', 'KZT', 'MAD', 'MDL', 'MNT', 'MXN', 'NOK',
               'NZD', 'PHP', 'PKR', 'PLN', 'QAR', 'RON', 'RSD',
               'SAR', 'SEK', 'SGD', 'SYP', 'THB', 'TJS', 'TMT',
               'TRY', 'UAH', 'USD', 'UZS', 'VES', 'ZAR')

#текст в обработку /help
TEXT_FOR_HELP = """
<b>Правильный формат</b> для ввода валют: <em>EUR</em>, <em>USD</em>, <em>RUB</em> и т.п.
"""

#создание функции, для проверки числа на float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #Создаем клавиатуру с тремя кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_conversion = types.KeyboardButton(text="конвертация")
    button_settings = types.KeyboardButton(text="настройки")
    button_help = types.KeyboardButton(text="/help")
    keyboard.add(button_conversion, button_settings, button_help)

    #Отправляем приветственный стикер
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEIsshkRVoN6Ub0abVPXUhS6zrxa9aQvgACAQEAAladvQoivp8OuMLmNC8E')

    # Отправляем приветственное сообщение с клавиатурой
    await message.answer("Привет! Я телеграмм бот для конвертации валют. Что будем делать?", reply_markup=keyboard)

#Обработка команды /help
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(TEXT_FOR_HELP, parse_mode="HTML")

#Обработка настройки
@dp.message_handler(text='настройки')
async def send_welcome(message: types.Message):
    await message.answer(TEXT_FOR_HELP, parse_mode="HTML")

#Создаем класс состояния
class UserState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

#Обработка сообщения конвертация и состояния from_currency
@dp.message_handler(text='конвертация')
async def data_for_convertation(message: types.Message):
    await message.answer("Введите валюту, из которой будет проводиться конвертация")
    await UserState.from_currency.set()

#Обработка состояния to_currency
@dp.message_handler(state=UserState.from_currency)
async def get_from_currency(message: types.Message, state: FSMContext):
    if message.text not in currencies:
        await message.answer("Такой валюты не существует, либо она не поддерживается. Попробуйте ещё раз.")
    else:
        await state.update_data(from_currency=message.text)
        await message.answer("Введите валюту, в которую будет проводиться конвертация")
        await UserState.next()

#Обработка состояния amount
@dp.message_handler(state=UserState.to_currency)
async def get_to_currency(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text not in currencies:
        await message.answer("Такой валюты не существует, либо она не поддерживается. Попробуйте ещё раз.")

    else:
        if message.text == data['from_currency']:
            await message.answer("Вы ввели одинаковые валюты. Попробуйте ещё раз")
        else:
            await state.update_data(to_currency=message.text)
            await message.answer("Введите сумму для конвертации")
            await UserState.next()

#Итог и конвертация
@dp.message_handler(state=UserState.amount)
async def get_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    if data['amount'].isdigit() == True or isfloat(data['amount']) == True:
        try:
            converted_amount = (int(data['amount']) / rates[data['from_currency']] * rates[data['to_currency']])
            await message.answer(f"{data['amount']} {data['from_currency']} = {converted_amount} {data['to_currency']}")
            await state.finish()
        except:
            converted_amount = (float(data['amount']) / rates[data['from_currency']] * rates[data['to_currency']])
            await message.answer(f"{data['amount']} {data['from_currency']} = {converted_amount} {data['to_currency']}")
            await state.finish()
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз")

#Запускаем бота, пропуская обновления
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)