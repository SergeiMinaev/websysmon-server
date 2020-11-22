#!/usr/bin/env python3
from get_system_state import get_state, update_state_files, get_prev_state
from telegram_bot import send_to_telegram
from utils import hostname

avail_perc_min = 5
iavail_perc_min = 5

def check_state():
    state = get_state()
    update_state_files(state)
    prev_state = get_prev_state()
    if not state:
        send_to_telegram(
            f'{hostname()}: ошибка: не удалось получить информацию о состоянии системы.')
        return

    for entity in state['entities']:
        for service in state['entities'][entity]['systemd_services'].items():
            if service[1]['status'] != 'active':
                send_to_telegram(
                    f'{entity}: сервис неактивен: {service[0]}.')
            elif prev_state['entities'][entity]['systemd_services']\
                    [service[0]]['status'] != 'active':
                send_to_telegram(
                    f'{entity}: сервис снова активен: {service[0]}.')

    for part in state['global']['partitions'].items():
        if part[1]['avail_perc'] < avail_perc_min:
            send_to_telegram(
                f'{hostname()}: на разделе {part[0]} свободно менее {avail_perc_min}%.')
        elif prev_state['global']['partitions'][part[0]]\
                ['avail_perc'] < avail_perc_min:
            send_to_telegram(
                f'{hostname()}: на разделе {part[0]} снова достаточно свободного места.')

        if part[1]['iavail_perc'] < iavail_perc_min:
            send_to_telegram(' '.join([
                f'{hostname()}: на разделе {part[0]} свободно менее',
                f'{iavail_perc_min}% инодов.']))
        elif prev_state['global']['partitions'][part[0]]\
                ['iavail_perc'] < iavail_perc_min:
            send_to_telegram(
                f'{hostname()}: на разделе {part[0]} снова достаточно свободных инодов.')

    for url in state['global']['urls'].items():
        if url[1]['status_code'] != 200:
            send_to_telegram(' '.join([
                f'{hostname()}: проблемы с доступностью {url[0]}:',
                f'код ответа - {url[1]["status_code"]}.']))
        elif prev_state['global']['urls'][url[0]]['status_code'] != 200:
            send_to_telegram(f'{hostname()}: {url[0]} снова доступен.')

if __name__ == '__main__':
    check_state()
