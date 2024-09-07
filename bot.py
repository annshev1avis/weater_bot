import telebot
from forecast import Forecast
from database import Database
import vulnarable_info

bot = telebot.TeleBot(vulnarable_info.telegram_token)
menu = [telebot.types.BotCommand('start', 'начни с этой команды'),
        telebot.types.BotCommand('day', '8:00-19:00'),
        telebot.types.BotCommand('evening', '16:00-23:00'),
        telebot.types.BotCommand('change_city', 'сменить город для прогноза')]
bot.set_my_commands(commands=menu)

db = Database()

@bot.message_handler(commands=['start'])
def send_info(message):
    bot.reply_to(message, "Привет! Я могу дать сводку погоды на весь день или для вечерней прогулки ")
    ask_city(message)

@bot.message_handler(commands=['change_city'])
def ask_city(message):
    bot.send_message(message.chat.id, "Ваш город:")
    bot.register_next_step_handler(message, update_city)

def update_city(message):
    city = message.text
    try:
        # если города с таким названием не существует или данных о нем нет в сервисе weatherapi - возникает исключение
        forecast = Forecast(city, 0, 0)
        db.update_chats_city(message.chat.id, city)
        bot.send_message(message.chat.id, f"Оки, город {city} запомнен")
    except:
        bot.reply_to(message, "Не могу найти такой город\n Попробуйте еще раз раз /change_city")

@bot.message_handler(commands=['day'])
def day_forecast(message):
    """отпраляет сводку погоды с 8:00 до 18:00"""

    forecast = Forecast(db.get_city(message.chat.id), 8, 18)
    bot.send_message(message.chat.id, forecast.day_summary_str())

@bot.message_handler(commands=['evening'])
def evening_forecast(message):
    forecast = Forecast(db.get_city(message.chat.id), 16, 23)
    bot.send_message(message.chat.id, f"закат: {forecast.get_sunset()}\n" +
                      forecast.day_summary_str())

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
db.disconnect()