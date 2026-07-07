from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
    InvalidCallbackData,
)
from Commands import (
    start_command,
    help_command
)
from Handlers import (
    message_handler,
    error,
    button_handler,
)
import os
from dotenv import find_dotenv, load_dotenv

# Getting environment variables

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")

# Main

if __name__ == "__main__":
    print("Starting...")
    app = Application.builder().token(TOKEN).base_url("https://tapi.bale.ai/").arbitrary_callback_data(True).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    # app.add_handler(CommandHandler("clear", clear_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    # app.add_handler(
    #     CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    # )

    # Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)