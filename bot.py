from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Updater, Dispatcher

from config import BOT_API_KEY
from websites import BrowserController


controller = BrowserController()
websites = controller.get_websites()


def start(update, context):
    kb = InlineKeyboardMarkup.from_column([InlineKeyboardButton(text=k,
                                                                callback_data='login:' + k)
                                           for k in websites])
    update.message.reply_text(
        'Приветствую! Выберите сайт, на котором пройти авторизацию!',
        reply_markup=kb)


def log_in_to_account(update: Update, context):
    call = update.callback_query
    name = call.data.split(':')[1]
    answer = 'Проходим авторизацию на сайте ' + name + '. Дождитесь завершения!'

    if name.lower() in ('wiq', 'smmkings'):
        answer += '\n\nДля входа на выбранном сайте необходимо пройти капчу, ' \
                  'поэтому авторизация может занять 1-3 минуты!'

    call.message.edit_text(answer)
    login = controller.login(name)
    call.message.reply_text('Авторизация прошла успешно. Логин: ' + login)


def cmd_create_ticket(update: Update, context):
    kb = InlineKeyboardMarkup.from_column([InlineKeyboardButton(text=k,
                                                                callback_data='create:' + k)
                                           for k in websites])
    update.message.reply_text(
        'Выберите сайт, на который нужно разместить ticket:',
        reply_markup=kb)


def choose_site_to_create_ticket(update: Update, context):
    call = update.callback_query
    name = call.data.split(':')[1]

    if not controller.check_if_logged_in(name):
        call.message.edit_text('Вы не залогинились на данном сайте, '
                               'воспользуйтесь командой /login '
                               'или выберете другой сайт!')
        return

    answer = 'Попытаемся разместить Тикет. Результат ' \
             'вы получите в виде ответа сервера - не пугайтесь!'
    call.message.edit_text(answer)

    response: dict = controller.create_ticket(name)

    formatted_response = '\n'.join(['{}: {}'.format(k.title(), str(v).title())
                                    for k, v in response.items()])

    call.message.reply_text('Вот что мы получили в ответ:\n\n' + formatted_response)


# conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
#                                    states={1: [CallbackQueryHandler(log_in_to_account)]},
#                                    fallbacks=[])
q_login_handler = CallbackQueryHandler(log_in_to_account, pattern='login:')
q_create_handler = CallbackQueryHandler(choose_site_to_create_ticket, pattern='create:')

start_handler = CommandHandler('start', start)
login_handler = CommandHandler('login', start)
create_handler = CommandHandler('create', cmd_create_ticket)
updater = Updater(BOT_API_KEY, use_context=True)
dp: Dispatcher = updater.dispatcher
dp.add_handler(start_handler)
dp.add_handler(q_login_handler)
dp.add_handler(q_create_handler)
dp.add_handler(login_handler)
dp.add_handler(create_handler)

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
