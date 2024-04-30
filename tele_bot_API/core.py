"""
Module: tele_bot_API/core.py
Description: Defines the operations and handlers for a Telegram bot,
including message handling, API interactions, and database operations.
"""

import telebot
import requests

from config import settings
from film_API.core import api_request
from database.core import crud
from database.common.models import db, Request
from tele_bot_API.util.messages import help_message, advanced_search_message, history_message

# Initialize the Telegram bot instance
bot = telebot.TeleBot(settings.telebot_token.get_secret_value())

# Initialize CRUD operations for the database
db_create_instance = crud.create()
db_read_instance = crud.read()

request = ""  # Global variable to store user requests


@bot.message_handler(commands=["start"])
def send_initial_message(message: telebot.types.Message) -> None:
    """
    Handle the '/start' command by sending an initial welcome message and prompting the user to choose a command.
    """
    bot.send_message(message.chat.id, f"Welcome to <b>{bot.get_my_name().name}</b> bot.\n", parse_mode="html")
    choose_command(message)


@bot.message_handler(commands=["hello-world"])
def send_hello_message(message: telebot.types.Message) -> None:
    """
    Handle the '/hello-world' command by sending a hello message.
    """
    bot.reply_to(message, f"Hello to you too!")


@bot.message_handler(func=lambda message: True)
def all_messages_handler(message: telebot.types.Message) -> None:
    """
    Handle all messages received by the bot.
    """
    global request
    request = message.text
    if message.text == "🎬 Film search (by title)":
        bot.send_message(
            message.chat.id,
            "Enter the full title of the movie in the next message (do not write anything other than the title)"
        )
        bot.register_next_step_handler(message, title_search)
    elif message.text == "🔎 Film advanced search (by params)":
        bot.send_message(
            message.chat.id,
            advanced_search_message,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, advanced_search)
    elif message.text == "🕒 Last arrivals":
        bot.send_message(
            message.chat.id,
            "Enter how many latest releases you want to receive (maximum 50, default 10)"
        )
        bot.register_next_step_handler(message, last_arrivals)
    elif message.text == "📜 History":
        bot.send_message(
            message.chat.id,
            "Enter how many recent requests you want to receive (maximum 10)"
        )
        bot.register_next_step_handler(message, history)
    elif message.text == "👋 Hello":
        response = f"Hello, {message.from_user.first_name}!"
        bot.reply_to(message, response)
        db_write_data(message.chat.id, request, response)
    elif message.text == "📞 Help":
        bot.send_message(
            message.chat.id,
            help_message.format(bot_name=bot.get_my_name().name),
            parse_mode="html"
        )
        db_write_data(message.chat.id, request, help_message.format(bot_name=bot.get_my_name().name))
        choose_command(message)
    else:
        response = "Unknown command!"
        bot.reply_to(message, response)
        db_write_data(message.chat.id, message.text, response)
        choose_command(message)


def choose_command(message: telebot.types.Message) -> None:
    """
    Prompt the user to choose a command from a predefined list of options.
    """
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    markup.add(
        "🎬 Film search (by title)",
        "🔎 Film advanced search (by params)",
        "🕒 Last arrivals",
        "📜 History",
        "👋 Hello",
        "📞 Help"
    )
    bot.send_message(message.chat.id, "Please, choose command from next list:", reply_markup=markup)


def title_search(message: telebot.types.Message) -> None:
    """
    Function for searching movie by title.
    """
    querystring = {"title": message.text}
    find_film_list = api_request("search", querystring)
    if not find_film_list:
        response_1 = "Movie with this title not found!"
        response_2 = "You can try again!"
        bot.send_message(message.chat.id, response_1)
        bot.send_message(message.chat.id, response_2)
        db_create_instance(message.chat.id, request, f"{response_1}\n\n{response_2}")
        choose_command(message)
    elif len(find_film_list) > 1:
        find_film = False
        for film in find_film_list:
            if film["title"] == message.text:
                film_details_sending(message, film)
                find_film = True
        if not find_film:
            response_1 = "You didn't give a very accurate name (too many coincidences)!"
            response_2 = "Next time, please be as precise as possible with the title of the movie!"
            bot.send_message(message.chat.id, response_1)
            bot.send_message(message.chat.id, response_2)
            db_create_instance(message.chat.id, request, f"{response_1}\n\n{response_2}")
            choose_command(message)
    else:
        film_details_sending(message, find_film_list[0])


def advanced_search(message: telebot.types.Message) -> None:
    """
    Function for searching movie by parameters.
    """
    lines = message.text.split("\n")

    params = {}
    for line in lines:
        key, value = line.split(": ")
        params[key.lower().replace(" ", "_")] = value

    count = 10
    if "count" in params:
        count = int(params.pop("count"))

    find_film_list = api_request("advancedsearch", params)
    for film in find_film_list[:count]:
        film_details_sending(message, film)


def last_arrivals(message: telebot.types.Message) -> None:
    """
    Function for displaying N latest arrivals from different platforms.
    """
    response = "This command doesn't work right now. You can choose any other."
    bot.send_message(message.chat.id, response)
    db_write_data(message.chat.id, request, response)
    choose_command(message)


def history(message: telebot.types.Message) -> None:
    """
    Function for displaying last N user's requests and their responses
    """
    last_n_records = db_read_instance(db, Request, message.chat.id, min(int(message.text), 10))
    last_n_records_list = [history_message.format(
        request=record.user_request, response=record.bot_response, datetime=record.created_at
    ) for record in last_n_records]
    for record in last_n_records_list:
        bot.send_message(message.chat.id, record, parse_mode="html")
    db_write_data(message.chat.id, request, "\n\n".join(last_n_records_list))


def film_details_sending(message: telebot.types.Message, film: dict[str: any]) -> None:
    """
    Function for finding and sending information about films
    """
    querystring = {"imdbid": film["imdbid"]}
    film_details = api_request("gettitleDetails", querystring)

    caption = ("Title: {title}\n"
               "IMDb ID: {imdbid}\n"
               "IMDb rating: {imdbrating}\n"
               "Runtime: {runtime}\n"
               "Released: {released}\n"
               "Genre: {genre}\n"
               "Synopsis: {synopsis}").format(
        title=film_details.get("title", ""),
        imdbid=film_details.get("imdbid", ""),
        imdbrating=film_details.get("imdbrating", ""),
        runtime=film_details.get("runtime", ""),
        released=film_details.get("released", ""),
        genre=", ".join(film_details.get("genre", [])),
        synopsis=film_details.get("synopsis", "")
    )

    db_write_data(message.from_user.id, f"{request}\n{message.text}", caption)

    try:
        if "imageurl" in film_details.keys() and film_details["imageurl"]:
            bot.send_photo(
                message.chat.id,
                requests.get(film_details["imageurl"][0]).content,
                caption=caption
            )
        else:
            bot.send_message(message.chat.id, caption)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, caption)


def db_write_data(user_id: int, user_request: str, bot_response: str) -> None:
    """
    Write user request and bot response to the database.

    :param user_id: The ID of the user making the request.
    :param user_request: The user's request.
    :param bot_response: The bot's response.
    """
    data = {
        "user_id": user_id,
        "user_request": user_request,
        "bot_response": bot_response
    }
    db_create_instance(db, Request, **data)


def bot_run() -> None:
    """
    Run the Telegram bot in infinite polling mode.
    """
    bot.infinity_polling()


if __name__ == "__main__":
    bot_run()
