#!/bin/env python3
import os
import json
import pytz
import subprocess
from shutil import copyfile
from datetime import datetime
from utils import service_manager_type, hostname
from telegram_bot import send_to_telegram

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(os.path.join(dir_path, "conf.json"))
conf = json.load(f)
f.close()


def now_utc_dt() -> datetime:
    return datetime.now(tz=pytz.utc)


def now_utc_ts() -> int:
    return int(datetime.now(tz=pytz.utc).timestamp())


def get_state():
    sm = service_manager_type()
    for entity in conf['entities']:
        print('Checking', entity, '...')
        if sm != 'systemd':
            send_to_telegram(' '.join([
                f'{hostname()}: ошибка: используемый менеджер сервисов - не systemd.',
                'Не удаётся узнать статус сервисов.',
                'Все сервисы помечены как неактивные.']))
        for service in conf['entities'][entity]['systemd_services']:
            cmd = f'systemctl is-active {service}; exit 0'
            if sm != 'systemd':
                status = 'inactive'
            else:
                status = subprocess.check_output(cmd, shell=True).decode().strip()
            conf['entities'][entity]['systemd_services'][service] = {"status": status}
    for part in conf['global']['partitions']:
        cmd = f'df --output=avail -B 1 {part} | tail -n 1'
        avail = int(subprocess.check_output(cmd, shell=True).decode().strip())
        cmd = f'df --output=size -B 1 {part} | tail -n 1'
        size  = int(subprocess.check_output(cmd, shell=True).decode().strip())
        cmd = f'df --output=itotal {part} | tail -n 1'
        itotal = int(subprocess.check_output(cmd, shell=True).decode().strip())
        cmd = f'df --output=iavail {part} | tail -n 1'
        iavail = int(subprocess.check_output(cmd, shell=True).decode().strip())

        conf['global']['partitions'][part] = {
            'size': size, 'avail': avail,
            'avail_perc': round(avail/size*100),
            'itotal': itotal, 'iavail': iavail,
            'iavail_perc': round(iavail/itotal*100),
        }


    conf['ts'] = now_utc_ts()

    return conf

def update_state_files(state):
    copyfile(
        os.path.join(dir_path, 'state.json'),
        os.path.join(dir_path, 'prev_state.json'))
    print('prev state saved')
    out = open(os.path.join(dir_path, 'state.json'), 'w')
    json.dump(conf, out)
    out.close()

def get_prev_state():
    return json.load(open(os.path.join(dir_path, 'prev_state.json'), 'r'))
