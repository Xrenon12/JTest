import datetime
import json

import subprocess
import sys
try:
    import telebot
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'telebot'])
finally:
    import telebot

# Инициализация переменных
initiator, start_time, test_run_time, host_name, file_name, stand, count_users, rampart, link, build_number, full = sys.argv
# initiator='jkl'
# start_time='kl;'
# test_run_time='kl;'
# host_name='kl;'
# file_name='kl;'
# stand='kl;'
# count_users=5
# rampart=5
# link='jkl'
# build_number=112
# full=False


bot = telebot.TeleBot('6148942898:AAFfzdCTZNQWvFjaccxtTIrJd7T8rta1Tqo')
data = {}
old_build = {}
params = ['sampleCount', 'errorPct', 'medianResTime', 'maxResTime', 'pct1ResTime']
localization = {
    'transaction': 'Транзакция',
    'sampleCount': 'Кол-во запросов',
    'errorCount': 'Кол-во ошибок',
    'errorPct': 'Процент ошибок',
    'meanResTime': 'Среднее время ответа (ms)',
    'medianResTime': 'Медиана времени ответа (ms)',
    'minResTime': 'Минимальное время ответа (ms)',
    'maxResTime': 'Максимальное время ответа (ms)',
    'pct1ResTime': 'Время отклика 90% (ms)',
    'pct2ResTime': 'Время отклика 95% (ms)',
    'pct3ResTime': 'Время отклика 99% (ms)',
    'throughput': 'Пропускная способность',
    'receivedKBytesPerSec': 'Получено Kb/сек',
    'sentKBytesPerSec': 'Отправлено Kb/сек'
}

def get_change(current, previous):
    if current == previous:
        return str('+ 0')
    try:
        result = round(((current - previous) / previous) * 100, 2)
        if result >= 0:
            return str('+' + str(result))
        else:
            return str('-' + str(result))
    except ZeroDivisionError:
        return str('+ 0')

# Чтение файла текущего билда
with open('D:\Jmeter\LastBuildResult\statistics.json', 'r') as f:
    d = json.load(f)

    for request in d:
        if request != 'Requests' and request != 'Total':
            data[request] = {}
            for key in d[request]:
                if key in params:
                    data[request][key] = d[request][key]
        elif request == 'Total':
            data[request] = {}
            for key in d[request]:
                if isinstance(d[request][key], float):
                    data[request][key] = round(d[request][key], 3)
                else:
                    data[request][key] = d[request][key]

# Чтение файла предыдущего билда
with open(f'D:\Jmeter\DashBoard{str(int(build_number)-1)}\statistics.json', 'r') as f:
    d = json.load(f)

    for request in d:
        if request != 'Requests' and request != 'Total':
            old_build[request] = {}
            for key in d[request]:
                if key in params:
                    old_build[request][key] = d[request][key]
        elif request == 'Total':
            old_build[request] = {}
            for key in d[request]:
                if isinstance(d[request][key], float):
                    old_build[request][key] = round(d[request][key], 3)
                else:
                    old_build[request][key] = d[request][key]

text = f'G1 Jmeter\n \nData: {datetime.datetime.now()} \n\n' \
        f'Start time: {start_time}\n' \
        f'Test run time (sec): {test_run_time}\n' \
        f'Host name: {host_name}\n' \
        f'file name: {file_name}\n' \
        f'Stand: {stand}\n' \
        f'Count users: {count_users}\n' \
        f'Rampart (sec): {rampart}\n' \
        f'Link: {link}\n\n'
if full == 'false':
    for i in data['Total']:
        if(i != 'transaction'):
            text += localization[i] + ' - ' + str(round(data['Total'][i], 3)) + ' (' + str(get_change(float(data['Total'][i]), float(old_build['Total'][i]))) + '%),\n'
else:
    for i in data:
        if i != 'Total':
            text += '\nTransaction: ' + i + '\n'
            for j in data[i]:
                try:
                    message_part = localization[j] + ' - ' + str(round(data[i][j], 3)) + ' (' + str(get_change(float(data[i][j]), float(old_build[i][j]))) + '%),\n'
                    text += message_part
                except:
                    message_part = localization[j] + ' - ' + str(round(data[i][j], 3)) + '\n'
                    text += message_part
img = open('D:/Jmeter/gra/gra-ResponseTimesDistribution.png', 'rb')
bot.send_photo(5107055135, img, caption=text)
# bot.send_message(5107055135, text)
