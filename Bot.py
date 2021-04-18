import os
from glob import glob
import telebot
from random import choice
TOKEN = '1715580463:AAGSuz7c8EKO43wt_0w6-Yfct8vcOfkVO6U'
PATH_SAVED_PICS = 'images_download_from_users'
PATH_GEN_PICS = 'images'
ANIME = 'anime'
name = ''
num = 0
photo_name = ''
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

def picturing(message, path):
    pic_list = glob(path + '/*')
    if message.text.isdigit() :
        if 1 <= int(message.text) <= len(pic_list):
            picture = pic_list[int(message.text) - 1]
            if os.path.exists(picture):
                photo = open(picture, 'rb')
                bot.send_photo(message.from_user.id, photo)
            else:
                bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')
        else:
            bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')
    else :
        bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')


def my_pic(message):
    picturing(message, PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}')

def pic(message):
    picturing(message, PATH_GEN_PICS)

def vid(message):
    webm_list = glob('webm/*')
    if 1 <= int(message.text) <= len(webm_list):
        webm = webm_list[int(message.text) - 1]
        if os.path.exists(webm):
            video = open(webm, 'rb')
            bot.send_video(message.from_user.id, video)
        else:
            bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')
    else:
        bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')

def photo_name_handler(message):
    global photo_name
    photo_name = message.text
    bot.send_message(message.from_user.id, 'Теперь загрузи фото')
    bot.register_next_step_handler(message, photo_handler)

def photo_handler(message):
    if photo_name != None :
        if os.path.exists(PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}/' + photo_name + '.jpg'):
            bot.send_message(message.from_user.id, 'Картинка с таким именем уже есть')
            default_photo_handler(message)
        elif message.text != '':
            if os.path.exists(PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}'):
                directory = PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}'
            else:
                os.mkdir(PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}')
                directory = PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}'
            photo = message.photo[-1]
            file_id = photo.file_id
            file_path = bot.get_file(file_id).file_path
            downloaded_file = bot.download_file(file_path)
            name = photo_name + ".jpg"
            new_file = open(directory + '/' + name, mode='wb')
            new_file.write(downloaded_file)
            new_file.close()
            bot.send_message(message.from_user.id, 'Принял photo_handler')
    else :
        bot.send_message(message.from_user.id, 'Просила же имя для пикчи, теперь она абракадаброй называется')
        default_photo_handler(message)





@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я догадываюсь, что тебя подослала Организация, чтобы выведать у меня секреты Хооина Кёмы")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Эль псай конгру")

@bot.message_handler(content_types=['voice'])
def handler(message):
    bot.send_message(message.chat.id, 'Напиши словами, не могу послушать')


@bot.message_handler(content_types=['photo'])
def default_photo_handler(message):
    if os.path.exists('images_from_users/{' + str(message.from_user.id) + '}'):
        directory = 'images_from_users/{' + str(message.from_user.id) + '}'
    else:
        os.mkdir('images_from_users/{' + str(message.from_user.id) + '}')
        directory = 'images_from_users/{' + str(message.from_user.id) + '}'
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = bot.get_file(file_id).file_path
    downloaded_file = bot.download_file(file_path)
    name = file_id + ".jpg"
    new_file = open(directory + '/' + name, mode='wb')
    new_file.write(downloaded_file)
    new_file.close()
    bot.send_message(message.from_user.id, 'Принял default photo')


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
    elif message.text == 'rand pic' :
        pic_list = glob(PATH_GEN_PICS + '/*')
        picture = choice(pic_list)
        photo = open(picture, 'rb')
        bot.send_photo(message.from_user.id, photo)
    elif message.text == 'pic' :
        pic_list = glob (PATH_GEN_PICS + '/*')
        textp = ''
        photo_num = 1
        for pic_name in pic_list :
            pic_name = pic_name[7:]
            textp = textp + ' ' + pic_name + ' - ' + str(photo_num) + '\n'
            photo_num += 1
        bot.send_message(message.from_user.id, 'Выбери номер фото из списка:' + textp)
        bot.register_next_step_handler(message, pic)
    elif message.text == 'rand webm' :
        webm_list = glob('webm/*')
        webm = choice(webm_list)
        video = open(webm, 'rb')
        bot.send_video(message.from_user.id, video)
    elif message.text == 'webm' :
        webm_list = glob ('webm/*')
        textw = ''
        webm_num = 1
        for webm_name in webm_list :
            webm_name = webm_name[5:]
            textw = textw + ' ' + webm_name + ' - ' + str(webm_num) + '\n'
            webm_num += 1
        bot.send_message(message.from_user.id, 'Выбери номер видео из списка:' + textw)
        bot.register_next_step_handler(message, vid)
    elif message.text == 'my pic' :
        path = PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}'
        if os.path.exists(path) :
            pic_list = glob(path + '/*')
            textp = ''
            photo_num = 1
            for pic_name in pic_list:
                pic_name = pic_name[39:]
                textp = textp + ' ' + pic_name + ' - ' + str(photo_num) + '\n'
                photo_num += 1
            bot.send_message(message.from_user.id, 'Выбери номер фото из списка:' + textp)
            bot.register_next_step_handler(message, my_pic)
        else :
            bot.send_message(message.from_user.id, 'Ты еще не отправлял мне фото')
    elif message.text == 'save pic' :
        bot.send_message(message.from_user.id, 'Придумай название для фото')
        bot.register_next_step_handler(message, photo_name_handler)
    elif message.text == '/anime':
        pic_list = glob(ANIME + '/*')
        picture = choice(pic_list)
        photo = open(picture, 'rb')
        bot.send_photo(message.from_user.id, photo)




bot.polling()
