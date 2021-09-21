from threading import Thread

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler
from telegram.ext import Updater, Dispatcher
from telegram.ext.filters import Filters

from config import BOT_API_KEY
from websites import BrowserController

controller = BrowserController()
websites = controller.get_websites()


class SpamThread(Thread):
    def __init__(self):
        self.update = None
        self._stop_event = False
        self.notified_finish = True
        self.tasks = []
        self.num = 0
        super().__init__(daemon=True)

    def add_task(self, tasks):
        self.tasks.clear()
        self.tasks.extend(tasks)
        self.num = len(self.tasks)
        self._stop_event = False
        self.notified_finish = False

    def set_update(self, update: Update = None):
        self.update = update

    def stop_event(self):
        self._stop_event = True
        self.notified_finish = True

    def is_working(self):
        return not self._stop_event and bool(self.tasks)

    def run(self):
        while True:
            while self._stop_event:
                continue

            n = 1
            while self.tasks:
                task = self.tasks.pop()

                if task.lower() in ('wiq', 'smmkings'):
                    self.update.message.reply_text(f'\u26D4 Следующий сайт {task} '
                                                   f'требует прохождения капчи, поэтому '
                                                   f'авторизация может занять чуть больше времени!')

                try:
                    name = controller.login(task)
                    message = controller.create_ticket(task)

                    if not self._stop_event:
                        self.update.message.reply_text(f'\u2705 {n}/{self.num}\n'
                                                       f'Сайт {task} завершил '
                                                       f'работу \n\n'
                                                       f'Логин: {name}\n\n'
                                                       f'Сообщение от сервера: {message}')
                    n += 1
                except Exception:
                    self.update.message.reply_text(f'Во время рассылки на сайте {task},'
                                                   f'произошла ошибка. Пропустили его.')
                    continue
            else:
                if not self.notified_finish:
                    self.update.message.reply_text('Спам рассылка закончилась')
                    self.notified_finish = True


def cmd_start_spam(update, context):
    if not context.user_data.get('theme', '').strip() or \
            not context.user_data.get('message', '').strip():
        update.message.reply_text(
            'Тема или сообщение тикета пусты! Пожалуйста, добавьте их командой /add')
        return

    if spam_thread.is_working():
        update.message.reply_text(
            'Нельзя начать новый спам-процесс, пока не закончен первый')
        return

    update.message.reply_text(
        'Вы успешно начали спам-рассылку. Дождитесь сообщений от сайтов.')

    spam_thread.set_update(update)
    spam_thread.add_task(websites)


def cmd_stop_spam(update, context):
    if not spam_thread.is_working():
        update.message.reply_text(
            'Процесс не запущен')
        return

    spam_thread.stop_event()

    update.message.reply_text(
        'Вы остановили процесс рассылки!')


spam_thread = SpamThread()
spam_thread.start()


def cmd_start(update, context):
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


def cmd_text_info(update, context):
    update.message.reply_text(
        f'Текущая тема тикета: {context.user_data.get("theme", "[не выбрано]")}\n'
        f'Текущее сообщение тикета: {context.user_data.get("message", "[не выбрано]")}')


def cmd_add_text(update, context):
    update.message.reply_text(
        'Введите тему тикета:')
    return 1


def choose_ticket_theme(update, context):
    context.user_data['theme'] = update.message.text
    update.message.reply_text(
        'Введите сообщение тикета:')
    controller.set_theme(update.message.text)

    return 2


def choose_ticket_message(update, context):
    context.user_data['message'] = update.message.text
    update.message.reply_text(
        'Данные тикета добавлены!')
    controller.set_message(update.message.text)

    return ConversationHandler.END


conv_handler = ConversationHandler(entry_points=[CommandHandler('add', cmd_add_text)],
                                   states={1: [MessageHandler(Filters.text, choose_ticket_theme,
                                                              pass_user_data=True)],
                                           2: [MessageHandler(Filters.text,
                                                              choose_ticket_message,
                                                              pass_user_data=True)]},
                                   fallbacks=[])
q_login_handler = CallbackQueryHandler(log_in_to_account, pattern='login:')
q_create_handler = CallbackQueryHandler(choose_site_to_create_ticket, pattern='create:')

start_handler = CommandHandler('start', cmd_start, pass_user_data=True)
login_handler = CommandHandler('login', cmd_start)
create_handler = CommandHandler('create', cmd_create_ticket)
start_spam_handler = CommandHandler('spam', cmd_start_spam, pass_user_data=True)
stop_spam_handler = CommandHandler('stop', cmd_stop_spam)
text_info_handler = CommandHandler('info', cmd_text_info, pass_user_data=True)

updater = Updater(BOT_API_KEY, use_context=True)
dp: Dispatcher = updater.dispatcher
dp.add_handler(start_handler)
dp.add_handler(q_login_handler)
dp.add_handler(q_create_handler)
dp.add_handler(login_handler)
dp.add_handler(create_handler)
dp.add_handler(stop_spam_handler)
dp.add_handler(start_spam_handler)
dp.add_handler(conv_handler)
dp.add_handler(text_info_handler)

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
