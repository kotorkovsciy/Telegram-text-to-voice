from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logging import basicConfig, INFO
from os import getenv
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=getenv('TOKEN'))
basicConfig(level=INFO)

dp = Dispatcher(bot, storage=MemoryStorage())
