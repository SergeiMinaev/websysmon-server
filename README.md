# websysmon
Minimalistic python system monitor with web interface (client-server)

# Requirements:
Python 3.8

# Installation:
$ git clone https://github.com/SergeiMinaev/websysmon_server.git
$ cd websysmon_server
$ cp example.conf.json conf.json
Edit conf.json:
  conf['entities'][yourproject'] - project's name;
  conf['entities'][yourproject']['systemd_services'] - list of systemd services to watch;
  conf['global']['partitions'] - list of partitions to watch.
Make a passwd.txt file to limiting access:
$ echo "somestrongpassword" > passwd.txt
Yes, this simple. Correct authentication is not the goal yet.

$ virtualenv ./venv
$ . virtualenv_activate.sh
$ pip install -r requirements.txt

# cp example.websysmon_server_start.sh /usr/local/bin/websysmon_server_start.sh
We copy it to /usr/local/bin/ to avoid potential SELinux restrictions.
Edit gunicorn_start.sh and specify correct paths in there.

Make it work as a system service. If you use systemd:
# cp example.websysmon_server.service /etc/systemd/system/websysmon_server.service
Edit it and specify correct paths, username and groupname.
