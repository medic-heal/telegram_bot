import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router             # Импорт основного роутера с обработчиками сообщений
from app.database.models import async_main  # Функция для инициализации базы данных

from decouple import config                 # Импорт конфигурации (для доступа к переменным из .env)

# Основная асинхронная функция, запускающая бота
async def main():
    await async_main()                      # Создание таблиц в БД при запуске (если их ещё нет)
    bot = Bot(config('TOKEN'))              # Создание объекта бота с токеном из .env
    dp = Dispatcher()                       # Создание диспетчера для маршрутизации событий
    dp.include_router(router)               # Подключение роутера с обработчиками команд
    await dp.start_polling(bot)             # Запуск бота (начало опроса Telegram-сервера)

# Точка входа в программу
if __name__ == '__main__':
    try:
        asyncio.run(main())                # Запуск основного цикла через asyncio
    except KeyboardInterrupt:
        print('Exit bot')                  # Корректное завершение работы при прерывании
