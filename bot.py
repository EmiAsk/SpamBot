from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Updater, Dispatcher

from config import BOT_API_KEY
from websites import Smm, SmmRaja, SmmIllusion, PeaKerr

WEBSITES = {'Smm': Smm, 'SmmRaja': SmmRaja, 'SmmIllusion': SmmIllusion, 'PeaKerr': PeaKerr}


def start(update, context):
    kb = InlineKeyboardMarkup.from_column([InlineKeyboardButton(text=k, callback_data=k)
                                           for k in WEBSITES])
    update.message.reply_text(
        'Приветствую! Выберите сайт, на котором пройти авторизацию!',
        reply_markup=kb)
    return 1


def log_in_to_account(update: Update, context):
    call = update.callback_query
    name = call.data
    browser = WEBSITES[name]
    call.message.edit_text('Проходим авторизацию на сайте ' + name + '. Дождитесь завершения!')
    login = browser().login()
    call.message.reply_text('Авторизация прошла успешно. Логин: ' + login)


# conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
#                                    states={1: [CallbackQueryHandler(log_in_to_account)]},
#                                    fallbacks=[])
q_handler = CallbackQueryHandler(log_in_to_account)
start_handler = CommandHandler('start', start)

updater = Updater(BOT_API_KEY, use_context=True)
dp: Dispatcher = updater.dispatcher
dp.add_handler(start_handler)
dp.add_handler(q_handler)

# from aiogram import Bot
# from aiogram.dispatcher.dispatcher import Dispatcher
# from aiogram.dispatcher.filters import Text
# from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
#
# from config import BOT_API_KEY
# from websites import Smm, SmmRaja, SmmIllusion, PeaKerr
#
# websites = {'Smm': Smm, 'SmmRaja': SmmRaja, 'SmmIllusion': SmmIllusion, 'PeaKerr': PeaKerr}

# bot = Bot(token=BOT_API_KEY)
# dp = Dispatcher(bot=bot)
#
#
# @dp.message_handler(commands=['start'])
# async def greet(message: Message):
#     kb = InlineKeyboardMarkup(row_width=1)
#     for k in websites:
#         kb.add(InlineKeyboardButton(k, callback_data=k))
#     await message.answer('Приветствую! Выберите сайт, на котором пройти авторизацию!',
#                          reply_markup=kb)
#
#
# @dp.callback_query_handler(Text(equals=list(websites.keys())))
# async def log_in_to_account(call: CallbackQuery):
#     name = call.data
#
#     browser = websites[name]
#
#     await call.message.edit_text('Проходим
#     авторизацию на сайте ' + name + '. Дождитесь завершения!')
#     await call.answer()
#
#     login = browser().login()
#
#     await bot.send_message(call.from_user.id, 'Авторизация прошла успешно. Логин: ' + login)
