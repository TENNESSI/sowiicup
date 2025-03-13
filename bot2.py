from gspread import Client, Spreadsheet, Worksheet, service_account
from config import token, table_id
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, CallbackQuery
from keyboards import GiveAddUsersKeyboard
from aiogram.enums import ParseMode
import json
from aiogram import F
import loguru
import threading

bot = Bot(token=token, parse_mode = "HTML")

dp = Dispatcher()

ADMIN_ID = 684882717 #аня
ADMIN_ID_2 = 1045401545 #я
ADMIN_ID_3 = 362124322 #настя
neteloks_id = 1041729764

def client_init_json() -> Client:
	return service_account(filename='sowiicup-a7b6607dcc6b.json')

client = client_init_json()
table = client.open_by_key(table_id)
title = table.worksheets()[0].title
worksheet = table.worksheet(title)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
	if message.from_user.id == ADMIN_ID or message.from_user.id == ADMIN_ID_3:
		await message.answer(f"Привет, Админ! @{message.from_user.username}", )
	else:
		await message.answer("Привет! Отправь свою анкету для регистрации на турнир по формату наже:\n\n1)ник с твича\n2)игровой ник\n3)ммр(как на вашем скрине)\n4)ид\n5) позиция\n6) быть кэпом да/нет\n\nНе забудь прикрепить скриншот ммр!!\n\nПРИМЕР АНКЕТЫ:")
		await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(f'images/example.jpg'), caption="1)mindluwa\n2)No Mercy\n3)14506\n4)1273483740\n5)4-5pos\n6)да",)
		print(f'Пользователь @{message.from_user.username} нажал /start')

@dp.message()
async def sendmsg(message: types.Message):
	if message.from_user.id != ADMIN_ID and message.from_user.id != ADMIN_ID_3 :
		# print(message.caption)
		# print(len(message.caption.split('\n')))
		if message.caption != None:
			if len(message.caption.split('\n')) == 6:
				twitch = message.caption.split('\n')[0][2:].strip()
				dotaname = message.caption.split('\n')[1][2:].strip()
				mmr = message.caption.split('\n')[2][2:].strip()
				dotaid = message.caption.split('\n')[3][2:].strip()
				pos = message.caption.split('\n')[4][2:].strip()
				captain = message.caption.split('\n')[5][2:].strip()
				data = [twitch, dotaname, mmr, dotaid, pos, captain, f'https://ru.dotabuff.com/players/{dotaid}', 'нет']
				print(f'Получена анкета от @{message.from_user.username} {message.from_user.id}')

				with open(f'players/forms/{message.from_user.id}.txt', 'w', encoding="utf-8") as file:
					file.writelines(f'{item}\n' for item in data)
					print(f'Данные от @{message.from_user.username} {message.from_user.id} во временном файле, ожидают подтверждения')

				await message.bot.download(file=message.photo[-1].file_id,
										   destination=f'images/{message.from_user.id}.jpg')
				print(f'Фото {message.from_user.id}.jpg успешно загружено')

				await bot.send_photo(chat_id=ADMIN_ID_3, photo=message.photo[-1].file_id,
									 caption=f"1){twitch}\n2){dotaname}\n3){mmr}\n4){dotaid}\n5){pos}\n6){captain}\nhttps://ru.dotabuff.com/players/{dotaid}",
									 reply_markup=GiveAddUsersKeyboard(message.from_user.id))
				# await bot.send_photo(chat_id=ADMIN_ID_2, photo=message.photo[-1].file_id,
				# 					 caption=f"1){twitch}\n2){dotaname}\n3){mmr}\n4){dotaid}\n5){pos}\n6){captain}\nhttps://ru.dotabuff.com/players/{dotaid}",
				# 					 reply_markup=GiveAddUsersKeyboard(message.from_user.id))
				# await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id,
				# 					 caption=f"1){twitch}\n2){dotaname}\n3){mmr}\n4){dotaid}\n5){pos}\n6){captain}\nhttps://ru.dotabuff.com/players/{dotaid}",
				# 					 reply_markup=GiveAddUsersKeyboard(message.from_user.id))
				# await bot.send_photo(chat_id=1303013337, photo=message.photo[-1].file_id,
				# 					 caption=f"1){twitch}\n2){dotaname}\n3){mmr}\n4){dotaid}\n5){pos}\n6){captain}\nhttps://ru.dotabuff.com/players/{dotaid}",
				# 					 reply_markup=GiveAddUsersKeyboard(message.from_user.id))
				await message.answer('жди пока примут')
			else:
				await message.answer('Неверный формат анкеты, попробуй снова или пожалуйся Ане')
		else:
			await message.answer('Анкета без скриншота!')

@dp.callback_query(F.data.startswith('add_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('add_','')

	old_caption = call.message.caption
	caption = old_caption + f'\n\n✅ПРИНЯТА (@{call.from_user.username})'
	with open(f'players/forms/{user_id}.txt', 'r', encoding="utf-8") as file:
		data = file.readlines()
		data[:] = [item.strip() for item in data]

	worksheet.append_row(data)
	print(f'Пользователь {user_id} добавлен в гугл таблицу')

	await bot.send_message(user_id, 'Ваша анкета принята!')
	await call.answer(f'Пользователь {user_id} добавлен.', show_alert=True)
	await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = caption)

@dp.callback_query(F.data.startswith('noadd_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('noadd_','')
	old_caption = call.message.caption
	caption = old_caption + f'\n\n🚫ОТКЛОНЕНА (@{call.from_user.username})'
	print(f'Пользователь {user_id} НЕ добавлен в гугл таблицу')
	await bot.send_message(user_id, 'Ваша анкета отклонена!')
	await call.answer(f'Пользователь {user_id} отклонён.', show_alert=True)
	await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = caption)

@dp.callback_query(F.data.startswith('ban_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('ban_','')
	await bot.send_message(user_id, 'Вы забанены! Пишите администратору')
	await call.answer(f'Пользователь {user_id} забанен.', show_alert=True)

async def main():
	await dp.start_polling(bot)

if __name__ == '__main__':
	client_init_json()
	asyncio.run(main())

# emoji="🎲"