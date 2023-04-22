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
    await message.answer("Привет! Я телеграмм бот для конвертации валют. Что будем делать?")

#Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)