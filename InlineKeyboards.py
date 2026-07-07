from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from Types import Place, SearchResult
from dotenv import find_dotenv, load_dotenv

# Getting environment variables

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

FRONT_BASE_URL = os.getenv("FRONT_BASE_URL")


def build_search_result_keyboard(search_results: list[Place]) -> InlineKeyboardMarkup:
    site_button = [InlineKeyboardButton("نتایج بیشتر در سایت", url = FRONT_BASE_URL)]
    buttons = [
        *[[InlineKeyboardButton(r.name, callback_data = SearchResult(r, search_results))] for r in search_results],
        site_button
    ]

    return InlineKeyboardMarkup(buttons)

def build_place_keyboard(place: SearchResult) -> InlineKeyboardMarkup:
    latitude, longitude, place_id = place.current_place.latitude, place.current_place.longitude, place.current_place.osm_id
    map_url = f"{FRONT_BASE_URL}/map/place?id={place_id}&lat={latitude}&lng={longitude}#c{latitude}-l{longitude}-16.00z-0p"

    buttons = [
        [InlineKeyboardButton("نظرات", callback_data = ("comments", place, 0))],
        [InlineKeyboardButton("مشاهده روی نقشه", url = map_url)],
        [InlineKeyboardButton("صفحه قبل", callback_data = ("back", place.places))]
    ]

    return InlineKeyboardMarkup(buttons)

def build_comment_keyboard(place: SearchResult, comment_number: int) -> InlineKeyboardMarkup:
    comments_count = len(place.current_place.comments)
    comment_select_buttons = []
    if comments_count != comment_number + 1:
        comment_select_buttons += [InlineKeyboardButton("نظر بعد", callback_data = ("comments", place, comment_number + 1))]
    if comment_number != 0:
        comment_select_buttons += [InlineKeyboardButton("نظر قبل", callback_data = ("comments", place, comment_number - 1))]

    if comment_select_buttons:
        buttons = [
            comment_select_buttons,
            [InlineKeyboardButton("صفحه قبل", callback_data = ("back", place))]
        ]
    else:
        buttons = [
            [InlineKeyboardButton("صفحه قبل", callback_data = ("back", place))]
        ]

    return InlineKeyboardMarkup(buttons)