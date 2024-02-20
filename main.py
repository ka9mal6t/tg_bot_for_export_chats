import os
import shutil

import pexpect
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TOKEN, APP_ID, APP_HASH

process = {}
PHONE, CODE, PASSWORD, START = range(4)
GLOBAL_PATH = os.getcwd() + "/"
PATH_FOLDER = "tg_history_dumper"
FILE_PATH = "/history"
reply_keyboard = [["RUN"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global process
    try:
        user_id = update.message.from_user.id

        if os.path.exists(GLOBAL_PATH + f"{user_id}" + PATH_FOLDER):
            shutil.rmtree(GLOBAL_PATH + f"{user_id}" + PATH_FOLDER)
        shutil.copytree(GLOBAL_PATH + PATH_FOLDER, GLOBAL_PATH + f"{user_id}" + PATH_FOLDER)
        os.chdir(GLOBAL_PATH + f"{user_id}" + PATH_FOLDER)
        command = "./tg_history_dumper"
        argument = ['-app-id', f'{APP_ID}', '-app-hash', f'{APP_HASH}']

        # Создаем объект-процесс, запускаем скрипт
        process[user_id] = pexpect.spawn(command, argument)

        await update.message.reply_text("Enter phone number: ",
                                        reply_markup=ReplyKeyboardRemove())

        process[user_id].expect("Enter phone number: ")
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True))
        return START
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global process
    user_id = update.message.from_user.id
    if process[user_id]:
        input_data = update.message.text
        process[user_id].sendline(input_data)
        await update.message.reply_text("Enter code: ")
        process[user_id].expect("Enter code: ")
    else:
        await update.message.reply_text("No active process. Use /start to initiate a new process.",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True))
        return START
    return CODE


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global process
    try:
        user_id = update.message.from_user.id
        if process[user_id]:
            input_data = update.message.text
            process[user_id].sendline(input_data)
            await update.message.reply_text("Enter password: ")
            process[user_id].expect("Enter password: ")
        else:
            await update.message.reply_text("No active process. Use /start to initiate a new process.")
            return START
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True))
        return START
    return PASSWORD


async def password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global process
    try:
        user_id = update.message.from_user.id
        if process[user_id]:
            input_data = update.message.text
            process[user_id].sendline(input_data)
            process[user_id].wait()
            process[user_id].close()

            for file in os.listdir(GLOBAL_PATH + f"{user_id}" + PATH_FOLDER + FILE_PATH):
                await context.bot.send_document(chat_id=user_id,
                                                document=open(
                                                    GLOBAL_PATH + f"{user_id}" + PATH_FOLDER + FILE_PATH + "/" + file,
                                                    'rb'))
            shutil.rmtree(GLOBAL_PATH + f"{user_id}" + PATH_FOLDER)
            os.chdir(GLOBAL_PATH)
        else:
            await update.message.reply_text("No active process. Use /start to initiate a new process.",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                             resize_keyboard=True))
            return START
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True)
                                        )
        return START
    return PASSWORD


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Canceled", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(filters.Regex("RUN"), start)],
            PHONE: [MessageHandler(filters.Regex("[0-9]+$"), phone)],
            CODE: [MessageHandler(filters.Regex("[0-9]+"), code)],
            PASSWORD: [
                MessageHandler(filters.Regex("^.{1,40}"), password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
