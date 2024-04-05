import os
import telebot
import mysql.connector
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()
BOT_TOKEN = "7179142718:AAGGEPnVE0HfzJU5NscGC7y3_KrpV1CyFbg"
bot = telebot.TeleBot(BOT_TOKEN)

#KONEKSI DATABASE
def connect_db():
    return  mysql.connector.connect(
    host='localhost',
    username='root',
    password='',
    database='db_ApiTelegram')

#INBOX
def inbox(username, message, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inbox (user_id, message, timestamp) VALUES (%s, %s, %s)", (username,  message, date))
    conn.commit()
    conn.close()

#OUTBOX
def outbox(username, message, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO outbox (user_id, message, timestamp) VALUES (%s, %s, %s)", (username,  message, date))
    conn.commit()
    conn.close()

def get_mahasiswa_by_nim(nim):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_mahasiswa WHERE nim = %s", (nim,))
    mahasiswa = cursor.fetchone()
    conn.close()
    return mahasiswa

def get_dosen_by_name(dosen_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_dosen WHERE nama LIKE %s", ('%' + dosen_name + '%',))
    dosen = cursor.fetchone()
    conn.close()
    return dosen

@bot.message_handler(commands=['cari_mhs'])
def cari_mahasiswa(m):
    answer = "Masukkan NIM mahasiswa yang ingin Anda cari:"
    bot.send_message(m.chat.id, answer)
    username = m.chat.id
    message = m.text
    date = datetime.now()
    inbox(username, message, date)
    outbox(username, answer, date)
    bot.register_next_step_handler(m, process_nim_input)

def process_nim_input(m):
    nim = m.text
    mahasiswa = get_mahasiswa_by_nim(nim)
    if mahasiswa:
        info_mahasiswa = f"NIM: {mahasiswa[0]}\nNama: {mahasiswa[1]}\nJurusan: {mahasiswa[3]}\nTanggal Lahir: {mahasiswa[2]}\nAngkatan: {mahasiswa[4]}"
        bot.send_message(m.chat.id, info_mahasiswa)
    else:
        bot.send_message(m.chat.id, "Maaf, mahasiswa dengan NIM tersebut tidak ditemukan.")

@bot.message_handler(commands=['cari_dosen'])
def cari_dosen(m):
    answer = "Masukkan nama dosen yang ingin Anda cari:"
    bot.send_message(m.chat.id, answer)
    username = m.chat.id
    message = m.text
    date = datetime.now()
    inbox(username, message, date)
    outbox(username, answer, date)
    bot.register_next_step_handler(m, process_dosen_name_input)

def process_dosen_name_input(m):
    dosen_name = m.text
    dosen = get_dosen_by_name(dosen_name)
    if dosen:
        info_dosen = f"NIP: {dosen[0]}\nNama Dosen: {dosen[1]}\nEmail: {dosen[2]}\nAlamat: {dosen[3]}"
        bot.send_message(m.chat.id, info_dosen)
    else:
        bot.send_message(m.chat.id, "Maaf, dosen dengan nama tersebut tidak ditemukan.")


#START
@bot.message_handler(commands=['start', 'hello'])
def start(m):
    answer ="Hallo selamat datang di bot buatan Paraboyy. Masukan perintah /show_menu untuk melihat daftar menu"
    bot.send_message(m.chat.id, answer)
    username = m.chat.id
    message = m.text
    date = datetime.now()
    inbox(username, message, date)
    outbox(username, answer, date)

#MENAMPILKAN MENU
@bot.message_handler(commands=['show_menu'])
def handle_show_menu(m):
    show_menu(m)

#PROSES CEK PERINTAH
@bot.message_handler(func=lambda message: True)
def handle_menu(m):
    option = m.text
    data = get_data_from_database(option, m)
    if data is not None:
        bot.send_message(m.chat.id, data)

#PROSES MENAMPILKAN MENU
def show_menu(m):
    options = get_menu_options()
    markup = types.ReplyKeyboardMarkup(row_width=1)
    for option in options:
        option_text = str(option[2]) 
        markup.add(types.KeyboardButton(option_text)) 
    bot.send_message(m.chat.id, "Pilih salah satu menu:", reply_markup=markup)
    username = m.chat.id
    message = m.text
    date = datetime.now()
    inbox(username, message, date)
    outbox(username, "Show menu", date)

#MEGAMBIL DATA MENU PADA DATABASE
def get_menu_options():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_menu")
    options = cursor.fetchall()
    conn.close()
    return options

def get_data_from_database(option, m):
    if option == "cari_mahasiswa":
        cari_mahasiswa(m)
        return None
    elif option == "cari_dosen":
        cari_dosen(m)
        return None
    elif option == "cari_gedung":
        cari_gedung(m)
        return None
    else:
        return "Maaf, perintah tidak dikenali."



bot.polling()