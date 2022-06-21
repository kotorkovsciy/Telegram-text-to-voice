from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=MemoryStorage())
