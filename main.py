import subprocess
import os
import shutil
from datetime import datetime, timedelta

data_path = 'Data/'


def strip_date(date):
    return date.replace('-', ' ').split()


def start_scraper(date):
    date = strip_date(date)
    processo = subprocess.Popen(['python3', f'web_scraper.py', f'--{date[0]}', f'--{date[1]}', f'--{date[2]}'])
    processo.communicate()


def start_gui():
    processo = subprocess.Popen(['python3', 'gui.py'])
    processo.wait()


def reset_data(date):
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.makedirs(data_path)
    if 'gathering_log.txt' in os.listdir():
        os.remove('gathering_log.txt')

    try:
        temp_data = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("DATA INVALIDA")
        return "DATA INVALIDA"

    if temp_data >= datetime.now():
        start_scraper(date)
    else:
        print("DATA INVALIDA")
        return "DATA INVALIDA"


if __name__ == '__main__':
    if len(os.listdir(data_path)) == 0:
        yesterday = datetime.now() - timedelta(days=1)
        start_scraper(yesterday.strftime('%Y-%m-%d'))
    start_gui()
