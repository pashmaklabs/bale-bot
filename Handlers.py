from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    CallbackContext,
    InvalidCallbackData,
)
from Types import (
    Place,
    SearchResult,
    create_mocked_data,
)
from InlineKeyboards import (
    build_search_result_keyboard,
    build_place_keyboard,
    build_comment_keyboard,
)
from CallbackPatterns import (
    back_pattern,
    result_display_pattern,
    comment_display_pattern,
)
import os
from dotenv import find_dotenv, load_dotenv

# Getting environment variables

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

BOT_USERNAME = os.getenv("BOT_USERNAME")

# Handlers

def response_handler(message: str, chat_type: str):
    """Checks and formats received messages from the user."""
    text = message.lower()

    # response = "در حال جستجو..."

    if chat_type == "group":
        if BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, "").strip()
        else:
            return ""

    return text

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = response_handler(update.message.text, update.message.chat.type)

    if not user_message:
        return

    response_message = await update.message.reply_text("دارم می گردم...")

    search_results = Place.get_places(user_message)[:5]
    # mocked_search_results = create_mocked_data()[:5]
    # search_results = mocked_search_results
    if search_results:
        response_text = "اینم چیز هایی که پیدا کردم (: با انتخاب هر کدوم می تونی جزئیاتش رو ببینی"

        await response_message.edit_text(response_text, reply_markup = build_search_result_keyboard(search_results))
    else:
        response_text = "چیزی که می خواستی رو نتونستم پیدا کنم ): جاهای دیگه رو امتحان کن"

        await response_message.edit_text(response_text)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    space = " " * 50 + "\u200D"
    image = None

    await query.answer()

    if back_pattern(query_data):
        if type(query_data[1]) == list:
            text = "اینم چیز هایی که پیدا کردم (: با انتخاب هر کدوم می تونی جزئیاتش رو ببینی"
            buttons = build_search_result_keyboard(query_data[1])
        else:
            query_data = query_data[1]

    if result_display_pattern(query_data):
        text, buttons, image = search_result_display_builder(query_data)
    elif comment_display_pattern(query_data):
        place, comment_number = query_data[1], query_data[2]
        text, buttons = comment_display_builder(place, comment_number)

    chat_id = update.effective_chat.id

    if query.message.photo or image:
        await query.delete_message()

        if image:
            await context.bot.send_photo(chat_id = chat_id, photo = image, caption = text, reply_markup = buttons)
        else:
            if len(text) < 50:
                text += space
            await context.bot.send_message(chat_id = chat_id, text = text, reply_markup = buttons)
    else:
        if len(text) < 50:
            text += space
        await query.edit_message_text(text = text, reply_markup = buttons)

    context.drop_callback_data(query)

def search_result_display_builder(choosen_search_result: SearchResult):
    """After user chooses a search result button, this function builds display of that result."""
    display_image = choosen_search_result.current_place.get_first_image_url()
    return str(choosen_search_result.current_place), build_place_keyboard(choosen_search_result), display_image

def comment_display_builder(place: SearchResult, comment_number: int):
    """After user chooses reading comments button, this function builds display of comments of that place."""
    if place.current_place.comments:
        comment = place.current_place.comments[comment_number]

        return str(comment), build_comment_keyboard(place, comment_number)
    else:
        return "نظری پیدا نشد ):", InlineKeyboardMarkup([[InlineKeyboardButton("صفحه قبل", callback_data = ("back", place))]])

async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "ببخشید، این دکمه از دسترس خارج شده ): دوباره دستور /start  یا چیزی که دنبالشی رو برام بفرست"
    )

# Error handler

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")