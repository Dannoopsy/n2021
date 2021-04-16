import telebot

TOKEN = '1715580463:AAGSuz7c8EKO43wt_0w6-Yfct8vcOfkVO6U'
name = ''
num = 0
bot = telebot.TeleBot(TOKEN)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Назови номер, данный тебе Окарином')
    bot.register_next_step_handler(message, reg_num)

def reg_num(message):
    global num
    while num == 0:
        try:
            num = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Назови номер сотрудника лаборатории гаджетов будущего')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я догадываюсь, что тебя подослала Организация, чтобы выведать у меня секреты Хооина Кёмы")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Эль псай конгру")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'привет' :
        bot.reply_to(message, 'Я здесь, понятно!?')
    elif message.text == 'Srbija' :
        bot.reply_to(message,'strong')
    elif message.text == 'слава роду' :
        bot.reply_to(message,'нет уроду')
    elif message.text == 'если есть на свете рай' :
        bot.reply_to(message, 'это - Краснодарский край')
    elif message.text == '/reg' :
        bot.send_message(message.from_user.id, 'Назови свое имя')
        bot.register_next_step_handler(message, reg_name)
    elif message.text == '/memory' :
        if name == '' :
            bot.send_message(message.from_user.id, 'Извините, я не знаю Вас')
        else :
            bot.send_message(message.from_user.id, name + ', перестань волноваться, я жива и помню тебя')


bot.polling()
