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

initiator, start_time, test_run_time, host_name, file_name, stand, count_users, rampart, link = sys.argv
bot = telebot.TeleBot('6148942898:AAFfzdCTZNQWvFjaccxtTIrJd7T8rta1Tqo')
data = {}
params = ['sampleCount', 'errorPct', 'medianResTime', 'maxResTime']
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

text = f'G1 Jmeter\n \nData: {datetime.datetime.now()} \n\n'
text += f'Start time: {start_time}\n' \
        f'Test run time (sec): {test_run_time}\n' \
        f'Host name: {host_name}\n' \
        f'file name: {file_name}\n' \
        f'Stand: {stand}\n' \
        f'Count users: {count_users}\n' \
        f'Rampart (sec): {rampart}\n' \
        f'Link: habr.com\n\n'
for i in data['Total']:
    text += localization[i] + ' - ' + str(data['Total'][i]) + ',\n'
bot.send_message(5107055135, text)