from tkinter import Image

from config import token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, CallbackQuery
from keyboards import StartKeyboard, GiveAddUsersKeyboard
from aiogram.enums import ParseMode
import json
from aiogram import F
import loguru
import threading

bot = Bot(token=token, parse_mode = "HTML")

dp = Dispatcher()

ADMIN_ID = 684882717
ADMIN_ID_2 = 1045401545
ADMIN_ID_3 = 362124322

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
	if message.from_user.id == ADMIN_ID or message.from_user.id == ADMIN_ID_3:
		await message.answer(f"Привет, Админ! @{message.from_user.username}", )
	else:
		await message.answer("Привет! Отправь свою анкету для регистрации на турнир по формату наже:\n\n1)ник с твича\n2)игровой ник\n3)ммр(как на вашем скрине)\n4)ид\n5) позиция\n6) быть кэпом да/нет\n\nНе забудь прикрепить скриншот ммр!!\n\nПример анкеты:")
		# await message.answer(text="1)mindluwa\n2)No Mercy\n3)14506\n4)1273483740\n5)4-5pos\n6)да", images = [FSInputFile(f'photos/example.jpg')])
		await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(f'photos/example.jpg'), caption="1)mindluwa\n2)No Mercy\n3)14506\n4)1273483740\n5)4-5pos\n6)да",)

@dp.message()
async def sendmsg(message: types.Message):
	if message.from_user.id != ADMIN_ID :
		# print(message.caption)
		# print(len(message.caption.split('\n')))
		if message.caption != None:
			if len(message.caption.split('\n')) == 6:
				twitch = message.caption.split('\n')[0][2:]
				dotaname = message.caption.split('\n')[1][2:]
				mmr = message.caption.split('\n')[2][2:]
				dotaid = message.caption.split('\n')[3][2:]
				pos = message.caption.split('\n')[4][2:]
				captain = message.caption.split('\n')[5][2:]
				await bot.send_photo(chat_id=ADMIN_ID_3, photo=message.photo[-1].file_id, caption=f"1){twitch}\n2){dotaname}\n3){mmr}\n4){dotaid}\n5){pos}\n6){captain}", reply_markup=GiveAddUsersKeyboard(message.from_user.id))
			else:
				await message.answer('Неверный формат анкеты, попробуй снова или пожалуйся Ане')
		else:
			await message.answer('Неверный формат анкеты, попробуй снова или пожалуйся Ане')

@dp.callback_query(F.data.startswith('add_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('add_','')
	await bot.send_message(user_id, 'Ваша анкета принята!')
	await call.answer(f'Пользователь {user_id} добавлен.', show_alert=True)

@dp.callback_query(F.data.startswith('noadd_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('noadd_','')
	await bot.send_message(user_id, 'Ваша анкета отклонена!')
	await call.answer(f'Пользователь {user_id} отклонён.', show_alert=True)

@dp.callback_query(F.data.startswith('ban_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('ban_','')
	await bot.send_message(user_id, 'Вы забанены! Пишите администратору')
	await call.answer(f'Пользователь {user_id} забанен.', show_alert=True)

async def main():
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())

# emoji="🎲"