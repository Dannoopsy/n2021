import os
from glob import glob
import telebot
from telebot import types
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

from random import choice
from db import *




TOKEN = '1715580463:AAGSuz7c8EKO43wt_0w6-Yfct8vcOfkVO6U'
PATH_GOOGLE = 'drive/MyDrive/'
PATH_SAVED_PICS = PATH_GOOGLE + 'images_download_from_users'
PATH_GEN_PICS = PATH_GOOGLE + 'images'
ANIME = PATH_GOOGLE + 'anime'     
WEBM = PATH_GOOGLE + 'webm'
photo_name = ''
bot = telebot.TeleBot(TOKEN)
key_name = 'Смотри чо ебану'

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('save pic')
itembtn2 = types.KeyboardButton('rand pic')
itembtn3 = types.KeyboardButton('rand webm')
itembtn4 = types.KeyboardButton('/help')
itembtn5 = types.KeyboardButton('count')
itembtn6 = types.KeyboardButton('list')
itembtn7 = types.KeyboardButton(key_name)
markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn7)

init_db()
if os.path.exists(PATH_GOOGLE + 'images_for_users'):
        pass
else:
        os.mkdir(PATH_GOOGLE + 'images_for_users')

if os.path.exists(PATH_SAVED_PICS):
        pass
else:
        os.mkdir(PATH_SAVED_PICS)

if os.path.exists(PATH_GOOGLE + 'images_from_users'):
        pass
else:
        os.mkdir(PATH_GOOGLE + 'images_from_users')



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
    webm_list = glob(WEBM + '/*')
    if 1 <= int(message.text) <= len(webm_list):
        webm = webm_list[int(message.text) - 1]
        if os.path.exists(webm):
            video = open(webm, 'rb')
            bot.send_video(message.from_user.id, video)
        else:
            bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')
    else:
        bot.send_message(message.from_user.id, 'Ты ввел некорректный номер')


#принимает первое фото

def photo_obj(message):
    if os.path.exists(PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'):
        directory = PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'
    else:
        os.mkdir(PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}')
        directory = PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_path = bot.get_file(file_id).file_path
        downloaded_file = bot.download_file(file_path)
        name_obj = file_id + '.jpg'
        new_file = open(directory + '/' + name_obj, mode='wb')
        new_file.write(downloaded_file)
        new_file.close()
        bot.send_message(message.from_user.id, 'Теперь пришли фото образец')
        bot.register_next_step_handler(message, photo_ex, name_obj)


#принимает второе фото и отправляет первое

def photo_ex(message, name_obj):
    if os.path.exists(PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'):
        directory = PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'
    else:
        os.mkdir(PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}')
        directory = PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}'
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_path = bot.get_file(file_id).file_path
        downloaded_file = bot.download_file(file_path)
        name = file_id + ".jpg"
        new_file = open(directory + '/' + name, mode='wb')
        new_file.write(downloaded_file)
        new_file.close()

        picture = PATH_GOOGLE + 'images_for_users/{' + str(message.from_user.id) + '}/' + name_obj 
        photo = open(picture, 'rb')
        bot.send_photo(message.from_user.id, photo)
    





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

            if message.photo:
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
    bot.send_message(message.from_user.id, text = 'Выбирай', reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Эль псай конгру' + '\n'+'Вот что я умею:' + '\n' + 'anime - рандомная аниме пикча'+ '\n' + 'webm - выбор видоса из общего хранилища' +
                 '\ncount - сколько сообщений ты мне прислал' + '\nlist - твои последние сообщения')

@bot.message_handler(content_types=['voice'])
def handler(message):
    bot.send_message(message.chat.id, 'Напиши словами, не могу послушать')


@bot.message_handler(content_types=['photo'])
def default_photo_handler(message):
    if os.path.exists(PATH_GOOGLE + 'images_from_users/{' + str(message.from_user.id) + '}'):
        directory = PATH_GOOGLE + 'images_from_users/{' + str(message.from_user.id) + '}'
    else:
        os.mkdir(PATH_GOOGLE + 'images_from_users/{' + str(message.from_user.id) + '}')
        directory = PATH_GOOGLE + 'images_from_users/{' + str(message.from_user.id) + '}'
    if message.photo:
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
    if message.text:
        add_message(user_id = message.from_user.id, text = message.text)
        #bot.send_message(message.from_user.id, text = 'Выбирай', reply_markup=markup)

    if message.text == 'привет' :
        bot.reply_to(message, 'Я здесь, понятно!?')
    elif message.text == 'Srbija' :
        bot.reply_to(message,'strong')
    elif message.text == 'слава роду' :
        bot.reply_to(message,'нет уроду')
    elif message.text == 'если есть на свете рай' :
        bot.reply_to(message, 'это - Краснодарский край')
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
            pic_name = pic_name[21:-4]
            textp = textp + ' ' + pic_name + ' - ' + str(photo_num) + '\n'
            photo_num += 1
        bot.send_message(message.from_user.id, 'Выбери номер фото из списка:\n' + textp)
        bot.register_next_step_handler(message, pic)
    elif message.text == 'rand webm' :
        webm_list = glob(WEBM + '/*')
        webm = choice(webm_list)
        video = open(webm, 'rb')
        bot.send_video(message.from_user.id, video)
    elif message.text == 'webm' :
        webm_list = glob (WEBM + '/*')
        textw = ''
        webm_num = 1
        for webm_name in webm_list :
            webm_name = webm_name[19:-4]
            textw = textw + ' ' + webm_name + ' - ' + str(webm_num) + '\n'
            webm_num += 1
        bot.send_message(message.from_user.id, 'Выбери номер видео из списка:\n' + textw)
        bot.register_next_step_handler(message, vid)
    elif message.text == 'my pic' :
        path = PATH_SAVED_PICS + '/{' + str(message.from_user.id) + '}'
        if os.path.exists(path) :
            pic_list = glob(path + '/*')
            textp = ''
            photo_num = 1
            for pic_name in pic_list:
                pic_name = pic_name[53:-4]
                textp = textp + ' ' + pic_name + ' - ' + str(photo_num) + '\n'
                photo_num += 1
            bot.send_message(message.from_user.id, 'Выбери номер фото из списка:\n' + textp)
            bot.register_next_step_handler(message, my_pic)
        else :
            bot.send_message(message.from_user.id, 'Ты еще не отправлял мне фото')
    elif message.text == 'save pic' :
        bot.send_message(message.from_user.id, 'Придумай название для фото')
        bot.register_next_step_handler(message, photo_name_handler)
    elif message.text == 'anime':
        pic_list = glob(ANIME + '/*')
        picture = choice(pic_list)
        photo = open(picture, 'rb')
        bot.send_photo(message.from_user.id, photo)
    if message.text == 'count' :
        nummes = str(count_message(user_id = message.from_user.id))
        bot.send_message(message.from_user.id, text = 'Столько ты отправил сообщений: ' + nummes[1:-2])
    if message.text == 'list' :
        nummes = int(str(count_message(user_id = message.from_user.id))[1:-2])
        nummes = min(nummes, 10)
        listmes = list_message(user_id = message.from_user.id, limit = nummes)
        stri = ''
        i = 0
        for mes in listmes:
            if i != 0:
                stri = stri + str(mes)[1:-2] + '\n'
            i = 1

        bot.send_message(message.from_user.id, 'Твои сообщения начиная с последнего:\n' + stri)
    if message.text == key_name :
        bot.send_message(message.from_user.id, 'Пришли фото, которое мы будем менять')
        bot.register_next_step_handler(message, photo_obj)
    '''if message.text:
        #add_message(user_id = message.from_user.id, text = message.text)
        bot.send_message(message.from_user.id, text = 'Выбирай', reply_markup=markup)
    '''


#bot.get_me()
bot.polling()
