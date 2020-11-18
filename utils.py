import os
import socket
import subprocess


def service_manager_type():
    cmd = 'ps --no-headers -o comm 1'
    return subprocess.check_output(cmd, shell=True).decode().strip()

def hostname():
    return socket.gethostname()
