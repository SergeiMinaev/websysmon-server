# websysmon
Minimalistic python system monitor with web interface (client-server)

# Requirements:
Python 3.7

# Installation:
$ git clone https://github.com/SergeiMinaev/websysmon_server.git
$ cd websysmon_server
$ cp example.conf.json conf.json
Edit conf.json:
  conf['entities'][yourproject'] - project's name;
  conf['entities'][yourproject']['systemd_services'] - systemd services to watch;
  conf['global']['partitions'] - list of partitions to watch.
Make a passwd.txt file to limiting access:
$ echo "somestrongpassword" > passwd.txt
Yes, this simple. Correct authentication is not the goal yet.

$ virtualenv ./venv
# Remember that minimum python version is 3.7. Set specific python binary if needed:
$ virtualenv --python=/opt/python37/bin/python3 ./venv
$ . virtualenv_activate.sh
$ pip install -r requirements.txt

Get the system state and write it to the file:
$ ./get_system_state.py
This will creates state.json file. This file contains information about current system
state. Not many details there because websysmon is pretty minimalistic.
Tell crontab to run it every minute. Use `crontab -e` and add this line in there:
`*/1 * * * * /path/to/websysmon_server/venv/bin/python /path/to/websysmon-server/get_system_state.py`
So state.json will be updating every minute.

$ sudo cp example.websysmon_server_start.sh /usr/local/bin/websysmon_server_start.sh
We copy it to /usr/local/bin/ to avoid potential SELinux restrictions.
Edit gunicorn_start.sh and specify correct paths in there.
Allow to run it by user if needed:
# sudo chmod 755 /usr/local/bin/websysmon_server_start.sh
Try to run it:
$ /usr/local/bin/websysmon_server_start.sh
If all works correct, you'll see this:
<...>
[INFO] Listening at: unix:</path/to/>websysmon_server/gunicorn.sock (11362)
<...>

Make it work as system service (it is assumed that you use systemd):
$ sudo cp example.websysmon_server.service /etc/systemd/system/websysmon_server.service
$ sudo chmod 644 /etc/systemd/system/websysmon_server.service
Edit it and specify correct paths, username and groupname.
Try to run it:
# service sm_websysmon_server start
# service sm_websysmon_server status
# systemctl is-active sm_websysmon_server
If all works correct, the last command's output will be "active".

Make it work besides Nginx:
# cp example.nginx.websysmon_server.conf /etc/nginx/conf.d/websysmon_server.conf
Edit it and specify paths and domain name.
Check nginx config:
$ nginx -t
If config test is successfull, restart nginx:
# service nginx restart

Try to open it with web-browser or with curl. 401 http code is ok because you not
authorized yet. If there is 502 bad gateway, check /var/log/nginx/websysmon_server.error_log.
If you see the line below, you should check permissions to the main dir (/path/to/websysmon_server).
"connect() to unix:/path/to/websysmon_server/gunicorn.sock failed (13: Permission denied) while
connecting to upstream"
# chmod 755 /path/to/websysmon_server
# service sm_websysmon_server restart
This should fix the problem.

Now you should be able to get the system state (raw JSON data) from the outside via curl like this:
curl -X POST -H "Content-Type: application/json" -d '{"passwd": yourpasswd}' http://domain.com

Telegram notifications
$ cp example.telegram_conf.json telegram_conf.json
Register new telegram bot via @BotFather.
Edit telegram_conf.json and specify bot's name and token.
Also specify contacts of users (username and telegram id) who will receive notifications.

