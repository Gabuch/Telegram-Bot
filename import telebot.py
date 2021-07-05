from sqlite3.dbapi2 import Connection, connect
import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot("1600322313:AAGARstCuiQE0mhSn0E7Z3O53k5yIQA_sK4")

conn = sqlite3.connect('C:\Program Files (x86)\SQLiteStudio\db', check_same_thread=False)
cursor = conn.cursor()

def db_select (user_id: int ):
    global results
    cursor.execute('select id from users where User_id = '+ str(user_id) + '  ORDER BY ID DESC LIMIT 1');
    
    results = cursor.fetchone()
    conn.commit()
    

def db_table_val(name: str,user_id: int , surname: str,otchestvo: str, email: str, tema: str, pol: str):    
    cursor.execute('INSERT INTO users (User_id, Name, Surname, otchestvo, Email, tema, pol) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, name, surname, otchestvo, email, tema, pol));
    conn.commit()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '1':
        global user_id;
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Для регистрации напишите цифру 1');

def get_name(message): #получаем имя
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id,'Какое у вас отчество');
    bot.register_next_step_handler(message, get_otchestvo);

def get_otchestvo(message): #получаем отчество
    global otchestvo;
    otchestvo = message.text;
    bot.send_message(message.from_user.id, 'Ваш Email?');
    bot.register_next_step_handler(message, get_email);

def get_email(message):
    global email;
    email = message.text;
    bot.send_message(message.from_user.id, 'Напишите тему обращения');
    bot.register_next_step_handler(message, get_tema);

def get_tema(message):    
    global tema;
    tema = message.text;
    bot.send_message(message.from_user.id, 'Опишите свое обращение');
    bot.register_next_step_handler(message, get_pol);

def get_pol(message): #получаем обращение
    global pol;
    pol = message.text;
    db_table_val( name=name, user_id = user_id, surname=surname, otchestvo=otchestvo, email=email,  tema = tema,pol = pol)
    db_select(user_id );
    bot.send_message(message.from_user.id, 'Ваше обращение записано под номером ' + str(results) + '.');
    bot.send_message(message.from_user.id, 'Спасибо за пользование нашей системой. Удачи');

bot.polling(none_stop=True)