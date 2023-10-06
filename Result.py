import datetime
import json
import os
import glob

import subprocess
import sys
try:
    import telebot
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'telebot'])
finally:
    import telebot

# test_run_time = 1
# host_name = 'R174'
# file_name = 'G1CreateBugReport.jmx'
# stand = 'stand'
# count_users = 1
# rampart = 1
# link = 'link'
# build_number = '165'
# full = 'true'

test_run_time = os.getenv("DURATION")
host_name = 'R174'
file_name = os.getenv("FileName")
stand = os.getenv("BASE_URL_2")
count_users = os.getenv("NUMBER_USERS")
rampart = os.getenv("RAMPART_SEC")
link = f'link'
build_number = os.getenv("BUILD_NUMBER")
full = os.getenv("FullResponse")

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
report_path = 'D:\Jmeter'
have_last_build = False

def imitation_table(headers:list, requests_data:object, last_build=False):
    result = ''
    max_length_col = [0] * (len(headers) + 1)

    # Определяем минимальную длинну
    for index, request_name in enumerate(requests_data):
        if max_length_col[0] <= len(request_name):
            max_length_col[0] = len(request_name) + 1
        for index, data in enumerate(requests_data[request_name]):
            if last_build:
                if max_length_col[index+1] <= len(data):
                    max_length_col[index+1] = len(data) + 1
                if max_length_col[index+1] <= len(requests_data[request_name][data]):
                    max_length_col[index+1] = len(requests_data[request_name][data]) + 1
            else:
                if max_length_col[index+1] <= len(data):
                    max_length_col[index+1] = len(data) + 1

    # Headers
    if len('Transaction ') < max_length_col[0]:
        result += 'Transaction' + (' ' * (max_length_col[0] - len('Transaction '))) + ' '

    for index, header_name in enumerate(headers):
        if len(header_name) < max_length_col[index+1]:
            result += header_name + (' ' * (max_length_col[index+1] - len(header_name)))
        if index == len(headers) - 1:
            result += '\n'

    for index, request_name in enumerate(requests_data):
        if max_length_col[0] > len(request_name):
            result += request_name + (' ' * (max_length_col[0] - len(request_name)))
        else:
            result += request_name
        for index, data_name in enumerate(requests_data[request_name]):
            if max_length_col[index+1] > len(str(requests_data[request_name][data_name])):
                result += str(requests_data[request_name][data_name]) + (' ' * (max_length_col[index+1] - len(str(requests_data[request_name][data_name]))))
            else:
                result += str(requests_data[request_name][data_name])
        if index != len(requests_data) - 1:
            result += '\n'
    return result

def get_change(current, previous):
    if current == previous:
        return str('+0')
    try:
        result = round(((current - previous) / previous) * 100, 2)
        if result >= 0:
            return str('+' + str(result))
        else:
            return str('-' + str(result))
    except ZeroDivisionError:
        return str('+0')


# Чтение файла текущего билда
with open(f'{report_path}\LastBuildResult\statistics.json', 'r') as f:
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

# Получаем последний прогон по выбранному файлу
files = glob.glob(pathname=f'{report_path}/DashBoard*{file_name}')
need_index = 0
last_build = 0
for index, name in enumerate(sorted(files)):
    number = int(name.split(' - ')[0].split('DashBoard')[1])
    if number > last_build and number != int(build_number):
        last_build = number
        need_index = index

if len(files) > 1:
    print('A file was used to compare the results: ' + files[need_index])
    have_last_build = True
    # Чтение файла предыдущего билда
    with open(f'{files[need_index]}\statistics.json', 'r') as f:
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

text_title = f'Gandiva Jmeter\n \nData: {datetime.datetime.now()} \n\n' \
             f'Test run time (sec): {test_run_time}\n' \
             f'Host name: {host_name}\n' \
             f'file name: {file_name}\n' \
             f'Stand: {stand}\n' \
             f'Count users: {count_users}\n' \
             f'Rampart (sec): {rampart}\n\n' \
             f'<a href="{link}">Jmeter results</a>\n\n'
text = ''
table_data = {}
if full == 'false':
    for i in data['Total']:
        if i != 'transaction':
            if len(files) > 1:
                text += localization[i] + ' - ' + str(round(data['Total'][i], 3)) + ' (' + str(get_change(float(data['Total'][i]), float(old_build['Total'][i]))) + '%)\n'
            else:
                text += localization[i] + ' - ' + str(round(data['Total'][i], 3)) + '\n'
else:
    for i in data:
        if i != 'Total':
            text += '\nTransaction: ' + i + '\n'
            table_data[i] = {}
            for j in data[i]:
                try:
                    message_part = localization[j] + ' - ' + str(round(data[i][j], 3)) + ' (' + str(get_change(float(data[i][j]), float(old_build[i][j]))) + '%)\n'
                    text += message_part
                    table_data[i][j] = str(round(data[i][j], 3)) + ' (' + str(get_change(float(data[i][j]), float(old_build[i][j]))) + '%)'
                except:
                    message_part = localization[j] + ' - ' + str(round(data[i][j], 3)) + '\n'
                    text += message_part
                    table_data[i][j] = str(round(data[i][j], 3))

table = f'<pre><code>{imitation_table(headers=params, requests_data=table_data, last_build=have_last_build)}</code></pre>'
if len(table) < 3900:
    if len(table + text_title) >= 1024:
        bot.send_message(text=text_title, chat_id=5107055135, parse_mode='HTML')
        bot.send_message(text=table, chat_id=5107055135, parse_mode='HTML')
    else:
        bot.send_message(text=text_title + table, chat_id=5107055135, parse_mode='HTML')
else:
    bot.send_message(text=text_title, chat_id=5107055135, parse_mode='HTML')

    if len(table) < 3900:
        bot.send_message(text=table, chat_id=5107055135, parse_mode='HTML')
    else:
        split_message = table.split('\n')
        summary_line = ''
        updated = False
        for index, line in enumerate(split_message):
            if (len(summary_line) + len(line)) < 4000:
                summary_line = summary_line + line + '\n'
                updates = False
            else:
                if index != len(split_message) - 1:
                    print(summary_line+'</pre></code>')
                    self.send_message(text=summary_line+'</pre></code>', chat_id=5107055135, parse_mode='HTML')
                else:
                    print(summary_line)
                    self.send_message(text=summary_line, chat_id=5107055135, parse_mode='HTML')
                summary_line = ''
                updated = True
            if updated is True:
                summary_line += '<pre><code>'
