#!/bin/env python3
from get_system_state import get_system_state
from telegram_bot import send_to_telegram
from utils import hostname

avail_perc_min = 5
iavail_perc_min = 5

def check_system_state():
    state = get_system_state()
    if not state:
        send_to_telegram(
            f'{hostname()}: ошибка: не удалось получить информацию о состоянии системы')
        return

    for entity in state['entities']:
        for service in state['entities'][entity]['systemd_services']:
            if state['entities'][entity]['systemd_services'][service]['status'] \
                    != 'active':
                send_to_telegram(
                    f'{entity}: сервис неактивен: {service}')
    for part in state['global']['partitions'].items():
        if part[1]['avail_perc'] < avail_perc_min:
            send_to_telegram(' '.join([
                f'{hostname()}: на разделе {part[0]} свободно менее {avail_perc_min}%',
                'свободного места.']))
        if part[1]['iavail_perc'] < iavail_perc_min:
            send_to_telegram(' '.join([
                f'{hostname()}: на разделе {part[0]} свободно менее',
                f'{iavail_perc_min}% инодов.']))

if __name__ == '__main__':
    check_system_state()
