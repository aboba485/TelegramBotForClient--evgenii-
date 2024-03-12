# Привет ,дорогой, написал этот код и комментарии к нему Арсений Атнашев Тимурович, когда будешь легко испровлять этот код, мысленно благодари меня))
# Также напоминаю, что оставил документ, для создания базы данных

from datetime import datetime, timedelta
import telebot

#получение токена
bot = telebot.TeleBot("6082784437:AAGfmHVMbiLZQXkZLq-20XA-W-9sO0nPwmE")

import sqlite3 as sq

# import sqlite3 as sq

# db = sq.connect('bd')
# cursor = db.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS promos(
# promos_name TEXT
# )""")

# cursor.execute("""CREATE TABLE IF NOT EXISTS used_promos(
# used_promos_name TEXT
# )""")

# cursor.execute("""CREATE TABLE IF NOT EXISTS nicks(
# name TEXT,
# good_time INTEGER
# )""")

# cursor.close()
# db.commit() 
# db.close()


#создание клавиатуры (для кнопок)
xochy_promo = telebot.types.ReplyKeyboardMarkup(True,True)
xochy_promo.row('Получить промокод','Перейти на bazium.ru')

#функция для отправки фотографии
def send_photo(message):
    photo = open('photo_basium.png', 'rb')
    bot.send_photo(message.chat.id, photo)
#функция для отправки приветственного сообщения
@bot.message_handler(commands=['start','bazium'])
def start(message):
    #подключение к базе данных (bd) и создание курсора
    db = sq.connect('bd')
    cursor = db.cursor() 
    #получение ника пользователя
    nick = message.from_user.username
    #проверка наличия пользователя в базе данных
    cursor.execute("SELECT name FROM nicks WHERE name=?", (nick,))
    #если пользователь не найден в базе данных
    if cursor.fetchone() is None:
        #отправляем приветственную картинку
        send_photo(message)
        #создание нового пользователя в базе данных
         
        #взятие промокода из базы данных
        cursor.execute("SELECT promos_name FROM promos LIMIT 1")
        promo = cursor.fetchone()
        cursor.execute("DELETE FROM promos WHERE promos_name=?", (promo[0],))
        cursor.execute("INSERT INTO used_promos (used_promos_name) VALUES (?)",(promo[0],))
        #преобразовываем промокод в тип данных string и удаляем от промокода ненужные сиволы 
        promo = str(promo)

        promo = promo.replace("'", '')  
        promo = promo.replace('(', '')
        promo = promo.replace(')', '')
        promo = promo.replace(',', '')
        #отслылаем сообщение с инструкцией по пользованию и самим промокодом. Также добавляем кнопки от клавиатуры 'xochy_promo'
        bot.send_message(message.chat.id,f'''
    <strong>Базиум + Яндекс.Бизнес = рост продаж</strong>

    5000 рублей бонуса на запуск новой рекламной кампании
    в Яндекс.Бизнес. Только для пользователей Базиума.

    Условия использования промокода:

    1. Рекламу можно запустить из системы управления Базиумом
    2. 5000 рублей добавляется при оплате 15000 рублей
    3. Промокод действует до 30 июня

    Ваш промокод:

    ------------

    <strong>{promo}</strong>

    ------------

    Использовать промокод можно на https://bazium.ru → Регистрация → Маркетинг → Яндекс.Бизнес
    ''', parse_mode='HTML',reply_markup=xochy_promo)

        #удаляем промокод из базы данных (потому - что он уже был использован)
        #получаем дату на данный момент
        now = datetime.now()
        #прибавляем к нему 59 минут и получаем минимальное время, когда пользоваетель с таким ником сможет еще раз получить промокод
        future_time = now + timedelta(minutes=59)
        good_time = future_time.strftime("%y/%m/%d/%H/%M")
        # обновляем дату для получения следующего промокода 
        cursor.execute("UPDATE nicks SET good_time=? WHERE name=?", (good_time, nick ,))
        #закрываем базу данных и курсор
        db.commit()
        cursor.close()
        db.close() 
    else:        
        #выбор времени по нику
        cursor.execute("SELECT good_time FROM nicks WHERE name = ?", (nick,))
        comparing_time = cursor.fetchone()[0]
        #время сейчас
        now = datetime.now()
        time_now = now.strftime('%y/%m/%d/%H/%M')
        #флаг если у нас был ник в базе
        if time_now>comparing_time:
        #Выполнение запроса на выборку данных
        # Выполнение запроса на выборку данных
            send_photo(message)
            cursor.execute("SELECT promos_name FROM promos LIMIT 1")
            promo = cursor.fetchone()
            cursor.execute("DELETE FROM promos WHERE promos_name=?", (promo[0],))
            cursor.execute("INSERT INTO used_promos (used_promos_name) VALUES (?)",(promo[0],))
            promo = str(promo)
            promo = promo.replace("'", '')  # replace unwanted characters
            promo = promo.replace('(', '')
            promo = promo.replace(')', '')
            promo = promo.replace(',', '')
            bot.send_message(message.chat.id, f"""
    <strong>Базиум + Яндекс.Бизнес = рост продаж</strong>

    5000 рублей бонуса на запуск новой рекламной 
    кампании в Яндекс.Бизнес. Только для пользователей Базиума.

    Условия использования промокода:

    1. Рекламу можно запустить из системы управления Базиумом
    2. 5000 рублей добавляется при оплате 15000 рублей
    3. Промокод действует до 30 июня

    Ваш промокод:

    ------------

    <strong>{promo}</strong>

    ------------

    Использовать промокод можно на https://bazium.ru → Регистрация → Маркетинг → Яндекс.Бизнес
""",parse_mode='HTML',reply_markup=xochy_promo)
            #получаем дату на данный момент
            now = datetime.now()
            #прибавляем к нему 59 минут и получаем минимальное время, когда пользоваетель с таким ником сможет еще раз получить промокод
            future_time = now + timedelta(minutes=59)
            good_time = future_time.strftime('%y/%m/%d/%H/%M')
            #обновляем дату для получения следующего промокода
            cursor.execute("UPDATE nicks SET good_time=? WHERE name=?", (good_time, nick ,))
            #закрываем базу данных и курсор
            cursor.close()
            db.commit() 
            db.close()
        #проверяем время на данный момент и сравниваем его с минимальеым временем для получения следующего промокода
        elif time_now<comparing_time:
            # подключение к базе данных (bd) и создание курсора
            db = sq.connect('bd')
            cursor = db.cursor()
            #выбор времени по нику
            nick = message.from_user.username 
            #взятие даты до которой нужно еще подождать
            cursor.execute("SELECT good_time FROM nicks WHERE name = ?", (nick,))
            needed_time = cursor.fetchone()
            now  = datetime.now()
            time_now = now.strftime('%y/%m/%d/%H/%M')
            good_time = needed_time[0]
            time_now_dt = datetime.strptime(time_now, '%y/%m/%d/%H/%M')
            good_time_dt = datetime.strptime(good_time, '%y/%m/%d/%H/%M')
            diff = good_time_dt - time_now_dt
            diff = diff//60
            diff = diff.total_seconds()
            diff = str(diff)
            diff = diff[:-2]  

            #отправление сообщения, где говориться до какого времени нужно подождать
            bot.send_message(message.chat.id, f'Мы не выдаем несколько промокодов сразу. Следующий можно получить через {diff} мин.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    #если юзер нажал кнопку - Получить промокод
    if message.text == 'Получить промокод':
        #подключение к базе данных 
        db = sq.connect('bd')
        cursor = db.cursor()
        nick = message.from_user.username
        #выбор времени по нику
        cursor.execute("SELECT good_time FROM nicks WHERE name = ?", (nick,))
        comparing_time = cursor.fetchone()[0]
        #время сейчас
        now = datetime.now()
        time_now = now.strftime('%y/%m/%d/%H/%M')
        #cравнение времени на данный момент и нужного времени
        if time_now>comparing_time:
                #отправление фотографии
                send_photo(message)
                #взятие промокода из базы данных
                cursor.execute("SELECT promos_name FROM promos LIMIT 1")
                promo = cursor.fetchone()
                #преобразовываем промокод в тип данных string и удаляем от промокода ненужные сиволы 
                cursor.execute("DELETE FROM promos WHERE promos_name=?", (promo[0],))
                cursor.execute("INSERT INTO used_promos (used_promos_name) VALUES (?)",(promo[0],))
                promo = str(promo)
                promo = promo.replace("'", '')  # replace unwanted characters
                promo = promo.replace('(', '')
                promo = promo.replace(')', '')
                promo = promo.replace(',', '')
                bot.send_message(message.chat.id, f"""
<strong>Базиум + Яндекс.Бизнес = рост продаж</strong>

5000 рублей бонуса на запуск новой рекламной кампании
в Яндекс.Бизнес. Только для пользователей Базиума.

Условия использования промокода:

1. Рекламу можно запустить из системы управления Базиумом
2. 5000 рублей добавляется при оплате 15000 рублей
3. Промокод действует до 30 июня 

Ваш промокод:

------------

<strong>{promo}</strong>

------------

Использовать промокод можно на https://bazium.ru → Регистрация → Маркетинг → Яндекс.Бизнес
""",parse_mode='HTML',reply_markup=xochy_promo)
                # время сейчас
                now = datetime.now()
                future_time = now + timedelta(minutes=59)
                good_time = future_time.strftime('%y/%m/%d/%H/%M')
                #обновляем дату для получения следующего промокода
                cursor.execute("UPDATE nicks SET good_time=? WHERE name=?", (good_time, nick ,))
                #закрываем базу данных и курсор
                cursor.close()
                db.commit() 
                db.close()
        #если время сейчас меньще, чем сравнимое
        elif time_now<comparing_time:
            #подключение к базе данных (bd) и создание курсора
            db = sq.connect('bd')
            cursor = db.cursor()
            #получение ника пользователя
            nick = message.from_user.username 
            #взятие даты до которой нужно еще подождать
            cursor.execute("SELECT good_time FROM nicks WHERE name = ?", (nick,))
            needed_time = cursor.fetchone()
            now  = datetime.now()
            time_now = now.strftime('%y/%m/%d/%H/%M')
            good_time = needed_time[0]
            time_now_dt = datetime.strptime(time_now, '%y/%m/%d/%H/%M')
            good_time_dt = datetime.strptime(good_time, '%y/%m/%d/%H/%M')
            diff = good_time_dt - time_now_dt
            diff = diff//60
            diff = diff.total_seconds()
            diff = str(diff)
            diff = diff[:-2]
            #отправление сообщения, где говориться до какого времени нужно подождать
            bot.send_message(message.chat.id, f'Мы не выдаем несколько промокодов сразу. Следующий можно получить через {diff} мин.', reply_markup=xochy_promo)
    #если юзер нажал кнопку <хочу на базиум>
    elif message.text == 'Перейти на bazium.ru':
        bot.send_message(message.chat.id, 'Класс! Вот ссылка на https://bazium.ru/', reply_markup=xochy_promo)
#бесконечное обновление бота
bot.infinity_polling() 
