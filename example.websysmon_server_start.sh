#!/bin/sh
/<path/to/websysmon_server>/venv/bin/gunicorn app --bind unix:/<path/to/websysmon_server>/gunicorn.sock --chdir <path/to/websysmon_server/> --log-level debug
