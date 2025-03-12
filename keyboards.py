from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

def StartKeyboard():
	pass

def GiveAddUsersKeyboard(id):
	# print(len(",".join(data).encode('utf-8')))
	button_yes = InlineKeyboardButton(text="Принять", callback_data = f'add_{id}')
	button_no = InlineKeyboardButton(text="Отклонить", callback_data = f'noadd_{id}',)
	button_ban = InlineKeyboardButton(text="БАН!!!", callback_data = f'ban_{id}')
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[button_yes, button_no], [button_ban]
	])
	return kb