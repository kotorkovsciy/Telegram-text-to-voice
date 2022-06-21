from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

butVoice = KeyboardButton('Перевести текст в голос')
butCancel = KeyboardButton('Отмена')


kbMainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
kbMainMenu.add(butVoice)

kbCancel = ReplyKeyboardMarkup(resize_keyboard=True)
kbCancel.add(butCancel)
