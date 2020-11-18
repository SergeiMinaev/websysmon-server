#!/bin/env python3

# curl -X POST -H 'Content-Type: application/json'  -d '{"chat_id": "-1001137499215", "text": "Сообщение из курла", "disable_notification": true}'    https://api.telegram.org/bot{токен}/sendMessage

import os
import json
import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
f = open(os.path.join(dir_path, 'telegram_conf.json'))
conf = json.load(f)
f.close()

token = conf['token']

def send_to_telegram(msg: str):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    for contact in conf['contacts']:
        data = {'chat_id': contact['id'], 'text': msg}
        r = requests.post(url, data=data)
        print(r.status_code, r.json())
