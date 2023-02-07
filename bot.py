import sqlite3


from telebot.async_telebot import AsyncTeleBot
#from telebot.custom_filters import TextFilter, TextMatchFilter, IsReplyFilter
bot = AsyncTeleBot('')



# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привет, этот бот сделан для номинаций года и трекинга поинтов, на данный момент бот ведет подсчет кринжпоинтов и респектпоинтов. \
Чтобы использовать бота, вы должны ответить на сообщение пользователя и написать кринж или респект. Выбор за вами! \
Чтобы мотивировать создателя продолжать что-то делать - можете скинуть ему свои деньги) \
""")


def insert_kring_points(username):
    try:
        sqliteConnection = sqlite3.connect('stats.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT username FROM kring_table WHERE username = ?", (username,))
        data=cursor.fetchall()
        points = 10
        if len(data) == 0:
            cursor.execute("INSERT INTO kring_table (username, points) VALUES (?, ?)", (username, points))
        else:
            cursor.execute("UPDATE 'kring_table' SET points = points - 10 WHERE username = ?", (username,))
            
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()        

def insert_krasava_points(username):
    try:
        sqliteConnection = sqlite3.connect('stats.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT username FROM krasava_table WHERE username = ?", (username,))
        data=cursor.fetchall()
        points = 10
        if len(data) == 0:
            cursor.execute("INSERT INTO krasava_table (username, points) VALUES (?, ?)", (username, points))
        else:
            cursor.execute("UPDATE 'krasava_table' SET points = points + 10 WHERE username = ?", (username,))

        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

@bot.message_handler(func=lambda message: message.reply_to_message is not None)
async def checker(message):
    emoji_cring = u'\U0001F602'
    emoji_respect = u'\U0001F929'
    emoji_coin = u'\U0001F4B8'
    if message.text.lower() == 'кринж':
        username = message.reply_to_message.from_user.username
        insert_kring_points(username)
        await bot.send_message(message.chat.id, (emoji_cring * 3) + "Пиздец! Все пользователи в ахуе что вы наделали: " + str(username) + " и вы получаете -10 кринжпоинтов" + (emoji_coin * 10))
    elif message.text.lower() == 'респект':
        username = message.reply_to_message.from_user.username
        insert_krasava_points(username)
        await bot.send_message(message.chat.id, (emoji_respect * 3) + "Воу! Очень хорошая работа: " + str(username) + " вам начисляется +10 респектпоинтов" + (emoji_coin * 10))
    else:
        pass

import asyncio
asyncio.run(bot.polling())
