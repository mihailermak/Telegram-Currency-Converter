#Token: 6183220089:AAF92022c-KAO_EAAcF3_TnsEfg5IxX0Rug

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

#Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

#Создаем бота и диспетчер
bot = Bot(token='6183220089:AAF92022c-KAO_EAAcF3_TnsEfg5IxX0Rug')
dp = Dispatcher(bot)

#Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #Создаем клавиатуру с двумя кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_conversion = types.KeyboardButton(text="Конвертация")
    button_settings = types.KeyboardButton(text="Настройки")
    keyboard.add(button_conversion, button_settings)

    #Отправляем приветственное сообщение с клавиатурой
    await message.answer("Привет! Я телеграмм бот для конвертации валют. Что будем делать?", reply_markup=keyboard)

#Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)