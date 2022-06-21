import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import voice


async def on_startup(_):
    logging.info("Бот вышел в онлайн")

voice.register_handlers_voice(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
