
from datetime import datetime
import json
import gdown
import os
import time
import tkinter as tk



def reader(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        return data


def get_garbage(trash):
    data = reader('data/trash_db.json')
    return data[trash]


def garbages_today(today):
    day = f'{today.year} {today.month} {today.day}'
    wrap = []

    for days in get_garbage("mixed"):
        if day in days:
            wrap.append('Mišrios atliekos')
    for days in get_garbage("paper"):
        if day in days:
            wrap.append('Popieriaus atliekos')
    for days in get_garbage("glass"):
        if day in days:
            wrap.append('Stiklo atliekos')
    return wrap


def mark_days(calendar):
    red_marked_dates, green_marked_dates = get_garbage('mixed'), get_garbage('paper')
    brown_marked_dates = get_garbage('glass')
    overlapping_dates = set()

    for date_str in red_marked_dates:
        date_obj = datetime.strptime(date_str, '%Y %m %d').date()
        calendar.calevent_create(date_obj, 'Garbage Day', tags='red')

    for date_str in green_marked_dates:
        date_obj = datetime.strptime(date_str, '%Y %m %d').date()
        if date_str in brown_marked_dates:
            overlapping_dates.add(date_str)
        else:
            calendar.calevent_create(date_obj, 'Garbage Day', tags='green')

    for date_str in brown_marked_dates:
        date_obj = datetime.strptime(date_str, '%Y %m %d').date()
        if date_str not in overlapping_dates:
            calendar.calevent_create(date_obj, 'Recycling Day', tags='brown')

    for date_str in overlapping_dates:
        date_obj = datetime.strptime(date_str, '%Y %m %d').date()
        calendar.calevent_create(date_obj, 'Both Events', tags='orange')

    calendar.tag_config('red', background='red', foreground='white')
    calendar.tag_config('green', background='green', foreground='white')
    calendar.tag_config('brown', background='brown', foreground='white')
    calendar.tag_config('orange', background='orange', foreground='black')


def data_downloader():
    file_id = '1DbQg6nxzWR7cjEY8cJ8BDLMGsLdfiB25'  # Replace with the actual file ID
    file_url = f'https://drive.google.com/uc?id={file_id}'
    output_file_name = 'data/trash_db.json'  # Change this to the desired output filename
    gdown.download(file_url, output_file_name, quiet=False)
    print(f'Downloaded: {output_file_name}')


def get_mod_date():
    file_path = 'data/trash_db.json'
    last_modified_time = os.path.getmtime(file_path)
    readable_time = time.ctime(last_modified_time)
    print(f"Last modified time of '{file_path}': {readable_time}")


def trash_by_day(today, window, header_font):
    if not garbages_today(today):
        garbage_sms_today = tk.Label(window,
                                     text=f'Šiandien ({today.year}-{today.month}-{today.day})\n šiukšlės nevežamos',
                                     font=header_font)
    else:
        garbage_sms_today = tk.Label(window, text=f'Šiandien ({today.year}-{today.month}-{today.day}) vežamos'
                                                  f'\n {garbages_today(today)}')
    garbage_sms_today.pack(pady=20)

    return garbage_sms_today
