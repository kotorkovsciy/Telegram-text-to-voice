from gtts import gTTS
from aiogram import Dispatcher, types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards import kbCancel, kbMainMenu
import speech_recognition as sr
from create_bot import bot
import subprocess
import os


class VOICE(StatesGroup):
    text = State()


async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kbMainMenu)


async def cmd_voice(message: types.Message, state: FSMContext):
    await VOICE.text.set()
    await message.answer('Введите текст/или отправте голосовое которое вы хотите форматировать в голос', reply_markup=kbCancel)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=kbMainMenu)


async def send_voice(message: types.Message, state: FSMContext):
    msg = await message.answer('Обрабатываю, ожидайте')
    await state.update_data(text=message.text)
    data_text = await state.get_data()
    obj = gTTS(text=data_text['text'], lang='ru', slow=False)
    obj.save(f'{message.from_user.id}.mp3')
    with open(f'{message.from_user.id}.mp3', "rb") as file:
        audio = file.read()
    await message.answer_audio(audio, title='Ваше голосовое сообщение', performer="Вы", reply_markup=kbMainMenu)
    await msg.delete()
    os.remove(f'{message.from_user.id}.mp3')
    await state.finish()


async def send_your_voice(message: types.Message, state: FSMContext):
    msg = await message.answer('Обрабатываю, ожидайте')
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'{message.from_user.id}.mp3')
    # with open(f'{message.from_user.id}.mp3', "rb") as file:
    #     audio = file.read()
    # await message.answer_audio(audio, title='Ваше голосовое сообщение', performer = "Вы", reply_markup=kbMainMenu)
    subprocess.call(['ffmpeg', '-i', f'{message.from_user.id}.mp3',
                     f'{message.from_user.id}.wav'])
    r = sr.Recognizer()
    file = sr.AudioFile(f'{message.from_user.id}.wav')
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio, language='ru')
    obj = gTTS(text=result, lang='ru', slow=False)
    obj.save(f'{message.from_user.id}2.mp3')
    with open(f'{message.from_user.id}2.mp3', "rb") as file:
        audio = file.read()
    await message.answer_audio(audio, title='Ваше голосовое сообщение', performer="Вы", reply_markup=kbMainMenu)
    await msg.delete()
    os.remove(f'{message.from_user.id}2.mp3')
    os.remove(f'{message.from_user.id}.mp3')
    os.remove(f'{message.from_user.id}.wav')
    await state.finish()


def register_handlers_voice(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_voice, Text(
        equals='Перевести текст в голос'), state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(
        equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(
        send_voice, state=VOICE.text, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        send_your_voice, state=VOICE.text, content_types=[ContentType.VOICE])
