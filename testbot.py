from aiogram.fsm.state import StatesGroup
from gspread import Client, Spreadsheet, Worksheet, service_account
from numpy.lib.function_base import extract
import os
from config import token, table_id
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery, ReplyKeyboardRemove
from keyboards import GiveAddUsersKeyboard, GiveStartKeyboard
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
admins = [ADMIN_ID, ADMIN_ID_3]
class UserStates(StatesGroup):
	twitch = State()
	dotaname = State()
	mmr = State()
	dotaid = State()
	pos = State()
	captain = State()
	screen = State()


def client_init_json() -> Client:
	return service_account(filename='sowiicup-a7b6607dcc6b.json')

client = client_init_json()
table = client.open_by_key(table_id)
title = table.worksheets()[0].title
worksheet = table.worksheet(title)

def is_banned(user_id):
	with open('players/banlist.txt', 'r', encoding='utf-8') as file:
		banlist = file.readlines()
		banlist = [item.strip() for item in banlist]
	if str(user_id) in banlist:
		return True
	else:
		return False

@dp.message(Command("banlist"))
async def cmd_get_banlist(message: types.Message):
	if message.from_user.id in admins:
		with open('players/banlist.txt', 'r', encoding='utf-8') as file:
			banlist = file.readlines()
			banlist = [item.strip() for item in banlist]
		await message.answer('\n'.join(banlist))

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
	await state.clear()
	if is_banned(message.from_user.id) == False:
		if message.from_user.id in admins:
			await message.answer(f"Привет, Админ! @{message.from_user.username}", )
		else:
			await message.answer("Привет! Чтобы зарегистрироватья на турнир, нажми на кнопку ниже!", reply_markup= GiveStartKeyboard())
			print(f'Пользователь @{message.from_user.username} нажал /start')

@dp.message(Command("unban"))
async def cmd_start(message: types.Message):
	if message.from_user.id in admins:
		if len(message.text.split(' '))==2:
			user_id = message.text.replace('/unban ', '')

			with open('players/banlist.txt', 'r', encoding='utf-8') as file:
				old_banlist = file.readlines()
				old_banlist = [item.strip() for item in old_banlist]
			new_banlist = []
			if user_id in old_banlist:
				for i in old_banlist:
					if i != user_id:
						new_banlist.append(i)

				with open('players/banlist.txt', 'w', encoding='utf-8') as file:
					for i in new_banlist:
						file.write(i+'\n')
				os.remove(f'players/forms/{user_id}.txt')

				await message.answer(f"разбанен {user_id}", )
			else:
				await message.answer(f'{user_id} не забанен')

@dp.message(StateFilter(None))
async def sendmsg(message: types.Message, state: FSMContext):
	if is_banned(message.from_user.id) == False:
		if message.text == 'Зарегистрироваться':
			if message.from_user.id not in admins:
				if worksheet.find(str(message.from_user.id)) != None:
					await message.answer('Твоя анкета уже зарегистрирована')
				else:
					if os.path.isfile(f'players/forms/{message.from_user.id}.txt') == True:
						await message.answer('Твоя анкета на проверке! За спам можно отлететь в бан.')
					else:
						await message.answer('Напиши свой ник на твиче', reply_markup=ReplyKeyboardRemove())
						await state.set_state(UserStates.twitch)

@dp.message(UserStates.twitch)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		await state.update_data(twitch=message.text)
		await message.answer('Записала. Теперь напиши свой игровой ник')
		await state.set_state(UserStates.dotaname)
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.dotaname)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		await state.update_data(dotaname=message.text)
		await message.answer('Молодец! Напиши сколько у тебя ммр точно')
		await state.set_state(UserStates.mmr)
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.mmr)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		if message.text.isdigit():
			await state.update_data(mmr=message.text)
			await message.answer('Отправь мне свой айди в доте')
			await state.set_state(UserStates.dotaid)
		else:
			await message.answer('В ответе должно быть число! Твой точный рейтинг')
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.dotaid)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		if message.text.isdigit():
			await state.update_data(dotaid=message.text)
			await message.answer('Скажи мне на какой позиции ты играешь. Напиши минимум две позиции(основную и дополнительную)')
			await state.set_state(UserStates.pos)
		else:
			await message.answer('В ответе должно быть число! Твой игровой айди из доты.')
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.pos)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		await state.update_data(pos=message.text)
		await message.answer('Ага, записала. Хочешь ли ты быть капитаном при распределении игроков на команды?')
		await state.set_state(UserStates.captain)
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.captain)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.text != None:
		await state.update_data(captain=message.text)
		await message.answer('Последний шаг. Отправь мне скриншот ммр')
		await state.set_state(UserStates.screen)
	else:
		await message.answer('В ответе должен содержаться текст')

@dp.message(UserStates.screen)
async def get_twitch(message: types.Message, state: FSMContext):
	if message.photo:
		await state.update_data(screen=message.photo[-1].file_id)

		user = await state.get_data()
		data = [user['twitch'], user['dotaname'], user['mmr'], user['dotaid'], user['pos'], user['captain'], f'https://ru.dotabuff.com/players/{user["dotaid"]}', 'нет',
				str(message.from_user.id)]
		print(f'Получена анкета от @{message.from_user.username} {message.from_user.id}')

		with open(f'players/forms/{message.from_user.id}.txt', 'w', encoding='utf-8') as file:
			file.writelines(f'{item}\n' for item in data)
			print(
				f'Данные от @{message.from_user.username} {message.from_user.id} во временном файле, ожидают подтверждения')

		await message.bot.download(file=user['screen'],
								   destination=f'images/{message.from_user.id}.jpg')
		print(f'Фото {message.from_user.id}.jpg успешно загружено')

		msg_ids = []
		chat_ids = []
		for admin in admins:
			msg = await bot.send_photo(chat_id=admin, photo=user['screen'],
									   caption=f"1) {user['twitch']}\n2) {user['dotaname']}\n3) {user['mmr']}\n4) {user['dotaid']}\n5) {user['pos']}\n6) {user['captain']}\nhttps://ru.dotabuff.com/players/{user['dotaid']}",
									   reply_markup=GiveAddUsersKeyboard(message.from_user.id))
			msg_ids.append(msg.message_id)
			chat_ids.append(str(admin))

		with open(f'players/forms/{message.from_user.id}.txt', 'a', encoding='utf-8') as file:
			file.write('_'.join([str(i) for i in msg_ids]) + "\n")
			file.write('_'.join(chat_ids))

		await message.answer('мур мур мур, твоя анкета на проверке.❤️')
		await state.clear()

	else:
		await message.answer('Отправль мне скриншот')

#кнопка принять анкету
@dp.callback_query(F.data.startswith('add_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('add_','')

	old_caption = call.message.caption
	caption = old_caption + f'\n\n✅ПРИНЯТА (@{call.from_user.username})'

	with open(f'players/forms/{user_id}.txt', 'r', encoding='utf-8') as file:
		data = file.readlines()
		data[:] = [item.strip() for item in data]
	chat_ids = [int(i) for i in data[-1].split('_')]
	msg_ids = [int(i) for i in data[-2].split('_')]

	worksheet.append_row(data[:-2])
	print(f'Пользователь {user_id} добавлен в гугл таблицу')

	await bot.send_message(user_id, 'Ваша анкета принята!')
	await call.answer(f'Пользователь {user_id} добавлен.', show_alert=True)
	for i in range(len(chat_ids)):
		await bot.edit_message_caption(chat_id=chat_ids[i], message_id=msg_ids[i], caption = caption)

#кнопка отклонить анкету
@dp.callback_query(F.data.startswith('noadd_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('noadd_','')
	old_caption = call.message.caption
	caption = old_caption + f'\n\n🚫ОТКЛОНЕНА (@{call.from_user.username})'
	with open(f'players/forms/{user_id}.txt', 'r', encoding='utf-8') as file:
		data = file.readlines()
		data[:] = [item.strip() for item in data]
	chat_ids = [int(i) for i in data[-1].split('_')]
	msg_ids = [int(i) for i in data[-2].split('_')]

	print(f'Пользователь {user_id} НЕ добавлен в гугл таблицу')
	await bot.send_message(user_id, 'Ваша анкета отклонена!', reply_markup=GiveStartKeyboard())
	await call.answer(f'Пользователь {user_id} отклонён.', show_alert=True)
	for i in range(len(chat_ids)):
		await bot.edit_message_caption(chat_id=chat_ids[i], message_id=msg_ids[i], caption = caption)
	os.remove(f'players/forms/{user_id}.txt')

@dp.callback_query(F.data.startswith('ban_'))
async def cancel(call: CallbackQuery):
	user_id = call.data.replace('ban_','')
	old_caption = call.message.caption
	caption = old_caption + f'\n\nБАНБАНБАНБАН (@{call.from_user.username})'

	with open(f'players/banlist.txt', 'a') as file:
		file.write(user_id+'\n')

	with open(f'players/forms/{user_id}.txt', 'r', encoding='utf-8') as file:
		data = file.readlines()
		data[:] = [item.strip() for item in data]
	chat_ids = [int(i) for i in data[-1].split('_')]
	msg_ids = [int(i) for i in data[-2].split('_')]

	await bot.send_message(user_id, 'Вы забанены! Пишите администратору')
	await call.answer(f'Пользователь {user_id} забанен.', show_alert=True)
	for i in range(len(chat_ids)):
		await bot.edit_message_caption(chat_id=chat_ids[i], message_id=msg_ids[i], caption = caption)

async def main():
	await dp.start_polling(bot)

if __name__ == '__main__':
	client_init_json()
	asyncio.run(main())

# emoji="🎲"