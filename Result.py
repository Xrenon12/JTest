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

bot = telebot.TeleBot('6148942898:AAFfzdCTZNQWvFjaccxtTIrJd7T8rta1Tqo')
data = {}
params = ['sampleCount', 'errorPct', 'medianResTime', 'maxResTime']
localization = {
    'transaction': 'Total',
    'sampleCount': 'Кол-во запросов',
    'errorCount': 'Кол-во ошибок',
    'errorPct': 'Процент ошибок',
    'meanResTime': 'Среднее время ответа',
    'medianResTime': 'Медиана времени ответа',
    'minResTime': 'Минимальное время ответа',
    'maxResTime': 'Максимальное время ответа',
    'pct1ResTime': 'Время отклика 90%',
    'pct2ResTime': 'Время отклика 95%',
    'pct3ResTime': 'Время отклика 99%',
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
for i in data['Total']:
    text += localization[i] + ' - ' + str(data['Total'][i]) + ',\n'
bot.send_message(5107055135, text)