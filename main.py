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

#Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #Создаем клавиатуру с двумя кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_conversion = types.KeyboardButton(text="конвертация")
    button_settings = types.KeyboardButton(text="настройки")
    keyboard.add(button_conversion, button_settings)

    #Отправляем приветственное сообщение с клавиатурой
    await message.answer("Привет! Я телеграмм бот для конвертации валют. Что будем делать?", reply_markup=keyboard)

#Создаем класс состояния
class UserState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

#Обработка сообщения о конвертации
@dp.message_handler(text='конвертация')
async def user_register(message: types.Message):
    await message.answer("Из какой валюты конвертировать?")
    await UserState.from_currency.set()


@dp.message_handler(state=UserState.from_currency)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("В какую валюту конвертировать?")
    await UserState.to_currency.set()


@dp.message_handler(state=UserState.amount)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("В какую валюту конвертировать?")
    await UserState.to_currency.set()


@dp.message_handler(state=UserState.to_currency)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(from_currency=message.text)
    data = await state.get_data()
    await message.answer("данные получены")

    await state.finish()

#Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)