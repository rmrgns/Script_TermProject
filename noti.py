#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

key = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg%3D%3D'
TOKEN = '6173459296:AAHHpKbnpemIXhsDw9XVLfMz8psPjuq_HL0'
MAX_MSG_LENGTH = 3000
baseurl = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2?serviceKey='+key
bot = telepot.Bot(TOKEN)

def getData(param):
    res_list = []
    url = baseurl+'&searchWrd='+quote(param)
    #print(url)
    #url = url.encode('utf-8')
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'xml')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[7]+'\n'+parsed[1]+'\n'+parsed[5]+'\n'+parsed[2]+'\n'+parsed[3]+'\n'+parsed[4] + '\n' + parsed[11]
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg, parse_mode='HTML')
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
