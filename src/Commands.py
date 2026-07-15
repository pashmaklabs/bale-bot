from telegram import Update
from telegram.ext import (
    ContextTypes,
)

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"سلام {user.first_name or ''} به پشمک خوش اومدی! هر جایی که می خوای بری رو توصیف کن تا برات پیداش کنم (:")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("lorem")

# async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Clears the callback data cache"""
#     context.bot.callback_data_cache.clear_callback_data()
#     context.bot.callback_data_cache.clear_callback_queries()
#     await update.effective_message.reply_text("All clear!")