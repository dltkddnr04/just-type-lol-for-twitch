from function import (irc_connect, function)
import random
import datetime
import math
import json
import time

file = open('config.json', 'r')
data = file.read()
data = json.loads(data)
file.close()
token, channel, nickname = data['token'], data['channel'], data['nickname']
if token == '' or channel == '' or nickname == '':
    print('Please fill in the config.json file')
    exit()

client_socket = irc_connect.set_socket(token, channel, nickname)

print('ready')

lol_count = 0
lol_list = []

once_check = False
lol_status = False
chat_delay = 2

while True:
    data = irc_connect.recive_data(client_socket)
    data = irc_connect.process_data(data)
    if data == 'PING':
        irc_connect.pong(client_socket)
    elif data != None:
        # print(data)

        data_type = function.count_alphabet(data[2])
        if data_type[0] > 0:
            lol_count += data_type[0]
            lol_list.append([datetime.datetime.now(), data[2]])
            chat_delay = chat_delay - 1
        elif data_type[1] > 0:
            # irc_connect.send_message(client_socket, channel, 'ㄹㅇㅋㅋ')
            pass

    # lol_list에서 최근 1분이내 리스트를 추출한다
    average_1, average_2 = function.get_average_data(lol_list, 60, 10, 'ㅋ')

    if average_1 < average_2:
        lol_status = True
    elif average_1 > average_2:
        lol_status = False
        once_check = False
        lol_list = []
        chat_delay = 2

    print('60_sec: {}, ten_sec: {}, delay: {}, status: {}'.format(math.ceil(average_1), average_2, chat_delay, lol_status))

    if lol_status == True and once_check == False:
        if chat_delay < 1:
            time.sleep(random.random())
            alphabet_average = function.get_alphabet_average(lol_list, 'ㅋ')
            irc_connect.send_message(client_socket, channel, 'ㅋ'*function.plus_minus(alphabet_average))
            print('{} type lol'.format(datetime.datetime.now()))
            # chat_delay = 2
            once_check = True
            