#!/bin/env python3
import os
import json
import pytz
import subprocess
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(os.path.join(dir_path, "conf.json"))
conf = json.load(f)
f.close()



def now_utc_dt() -> datetime:
    return datetime.now(tz=pytz.utc)


def now_utc_ts() -> int:
    return int(datetime.now(tz=pytz.utc).timestamp())


for entity in conf['entities']:
    print('Checking', entity, '...')
    for service in conf['entities'][entity]['systemd_services']:
        status = 'active'
        print(f'{service} is {status}')
        conf['entities'][entity]['systemd_services'][service] = {"status": status}



for part in conf['global']['partitions']:
    cmd = f'df --output=avail -B 1 {part} | tail -n 1'
    free_space = int(subprocess.check_output(cmd, shell=True).decode().strip())
    print(f'Amount of space in {part}: {free_space} bytes')
    conf['global']['partitions'][part] = {"avail": free_space}


conf['ts'] = now_utc_ts()
out = open(os.path.join(dir_path, "state.json"), "w")
json.dump(conf, out)
out.close()
