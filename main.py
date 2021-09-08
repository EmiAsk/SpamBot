# from aiogram import executor
# from bot import dp
from bot import updater


if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True)
    updater.start_polling(drop_pending_updates=True)
    updater.idle()