# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import requests
import json
import random
import os

# import os, shutil
# import os.path
import config
from updates_info import *
from db_operation import OperationDb
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

# from telebot.custom_filters import TextFilter, TextMatchFilter, IsReplyFilter
bot = AsyncTeleBot(os.environ.get("TELEGRAM_TOKEN"))
token_kino = os.environ.get("KINOPOISK_TOKEN")
movies_kinopoisk = config.MOVIES
korushki_names = config.NAMES

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привет, этот бот сделан для номинаций года и трекинга поинтов, на данный момент бот ведет подсчет кринжпоинтов и респектпоинтов. \
Чтобы использовать бота, вы должны ответить на сообщение пользователя и написать кринж или респект. Выбор за вами! \
Чтобы мотивировать создателя продолжать что-то делать - можете скинуть ему свои деньги) \
""")

@bot.message_handler(commands=['chat_info'])
async def send_chat_info(message):
    await bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['updates'])
async def send_updates(message):
    await bot.reply_to(message, info_message)

@bot.message_handler(commands=['movies'])
async def send_movies(message):

    keyboard_movies = InlineKeyboardMarkup(row_width=2)
    add_movies = []
    for first_pos, second_pos in zip(movies_kinopoisk, movies_kinopoisk[1:]):
        if first_pos in add_movies:
            pass
        else:
            keyboard_movies.add(InlineKeyboardButton(first_pos, callback_data=first_pos), InlineKeyboardButton(second_pos, callback_data=second_pos))
            add_movies.extend([first_pos, second_pos])
    await bot.send_message(message.chat.id, 'Выберите жанр:', disable_notification=True, reply_markup=keyboard_movies)

@bot.callback_query_handler(func=lambda call: call.data in movies_kinopoisk)
async def query_handler_answer_movies(call):

    category_movie = call.data

    myUrl = 'https://api.kinopoisk.dev/movie?field=rating.imdb&search=7-10&search=%s&field=genres.name&token=%s' % (category_movie, token_kino)
    response = requests.get(myUrl)
    json_data = json.loads(response.text)
    pages = json_data["pages"]

    #random pages for future search
    random_num_pages = random.randint(1, int(pages)-1)

    random_num_film = random.randint(0, 9)

    url_search = 'https://api.kinopoisk.dev/movie?field=rating.imdb&search=7-10&search=%s&field=genres.name&page=%s&limit=10&token=%s' % (category_movie, random_num_pages, token_kino)
    response_search = requests.get(url_search)
    json_data_search = json.loads(response_search.text)
    json_film_search = json_data_search['docs'][random_num_film]
    if json_film_search['name'] == None:
        film_name = json_film_search['alternativeName']
    else:
        film_name = json_film_search['name']

    film_rating = json_film_search['rating']['imdb']

    url = 'https://www.kinopoisk.ru/film/%s' % (json_film_search['id'])

    await bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup='')
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(call.message.chat.id, film_name + "\n" + "Рейтинг фильма: " + str(film_rating) + "\n" + "Ссылка на фильм: " + url)

# TODO: show stats about respect and cringe people

#@bot.message_handler(commands=['cringe_list'])
# async def send_welcome(message):
#    await bot.reply_to(message, """\
# Привет, этот бот сделан для номинаций года и трекинга поинтов, на данный момент бот ведет подсчет кринжкоинов и респекткоинов\
# """)

@bot.message_handler(commands=['ченнинг'])
async def button_message(message):
    if message.from_user.id == 306643703:
        keyboard_names = InlineKeyboardMarkup(row_width=3)
        add_users = []
        for first_pos, second_pos, third_pos in zip(korushki_names, korushki_names[1:], korushki_names[2:]):
            if first_pos in add_users:
                pass
            else:
                keyboard_names.add(InlineKeyboardButton(first_pos, callback_data=first_pos), InlineKeyboardButton(second_pos, callback_data=second_pos), InlineKeyboardButton(third_pos, callback_data=third_pos))
                add_users.extend([first_pos, second_pos, third_pos])
        await bot.send_message(message.chat.id, 'Выбери своего чемпиона:', disable_notification=True, reply_markup=keyboard_names)
    else:
        pass


@bot.callback_query_handler(func=lambda call: call.data in korushki_names)
async def query_handler_answer(call):

    if call.message.chat.id == 306643703:

        await bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup='')
        await bot.delete_message(call.message.chat.id, call.message.id)

        global username_for_tanya, key_points
        key_points = ["1", "2", "3"]

        username_for_tanya = call.data

        keyboard_points = InlineKeyboardMarkup()
        keyboard_points.add(InlineKeyboardButton(1, callback_data="1"),
                            InlineKeyboardButton(10, callback_data="2"),
                            InlineKeyboardButton(100, callback_data="3"),)

        await bot.send_message(call.message.chat.id, 'Чем тяжелее испытание, тем больше потом награда. Выбери награду своему чемпиону!', disable_notification=True, reply_markup=keyboard_points)
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Немедленно прекратите тыкать кнопки! Вы не Таня! Ваше время еще придет!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data in key_points)
async def query_handler_answer_points(call):

    await bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup='')
    await bot.delete_message(call.message.chat.id, call.message.id)

    if call.message.chat.id == 306643703:
        if call.data == "1":
            ins_func_one = OperationDb(username_for_tanya, 1, config.TANYA_TABLE)
            ins_func_one.insert_krasava_points()
            await bot.send_message(call.message.chat.id, "Давайте поздравим " + "корюшка " + str(username_for_tanya) + " с 1 таняпоинтом" + (
                        config.EMOJI_LIPTON * 1))
        elif call.data == "2":
            ins_func_ten = OperationDb(username_for_tanya, 10, config.TANYA_TABLE)
            ins_func_ten.insert_krasava_points()
            await bot.send_message(call.message.chat.id, "Давайте поздравим " + "корюшка " + str(username_for_tanya) + " с 10 таняпоинтами" + (
                        config.EMOJI_LIPTON * 5))
        elif call.data == "3":
            ins_func_hundred = OperationDb(username_for_tanya, 100, config.TANYA_TABLE)
            ins_func_hundred.insert_krasava_points()
            await bot.send_message(call.message.chat.id, "Давайте поздравим " + "корюшка " + str(username_for_tanya) + " с 100 таняпоинтами" + (
                        config.EMOJI_LIPTON * 10))
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Немедленно прекратите тыкать кнопки! Вы не Таня! Ваше время еще придет!", show_alert=True)

@bot.message_handler(func=lambda message: message.reply_to_message is not None)
async def checker(message):

    if message.text.lower() == 'кринж':
        username = message.reply_to_message.from_user.username
        ins_func_cring = OperationDb(username, 10, config.DISRESPECT_TABLE)
        ins_func_cring.insert_kring_points()
        await bot.send_message(message.chat.id,
                               (
                                           config.EMOJI_CRING * 3) + "Пиздец! Все пользователи в ахуе что вы наделали: " + str(username) + " и вы получаете -10 кринжпоинтов" + (
                                           config.EMOJI_COIN * 10))
    elif message.text.lower() == 'респект':
        username = message.reply_to_message.from_user.username
        ins_func_respect = OperationDb(username, 10, config.RESPECT_TABLE)
        ins_func_respect.insert_krasava_points()
        await bot.send_message(message.chat.id, (
                    config.EMOJI_RESPECT * 3) + "Воу! Очень хорошая работа: " + str(username) + " вам начисляется +10 респектпоинтов" + (
                                           config.EMOJI_COIN * 10))
    else:
        pass


import asyncio

asyncio.run(bot.polling())