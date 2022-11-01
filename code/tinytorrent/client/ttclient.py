import os, sys
import psutil
import argparse
import subprocess

from subprocess import DEVNULL

DAEMON_PORT = 6667
DAEMON_NAME = 'ttdaemon'
DAEMON_PATH = '../daemon/'

def checkDaemonRunning():
    for proc in psutil.process_iter():
        try:
            if DAEMON_NAME in proc.name().lower():
                print('Daemon process found.\n')
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def startDaemon():
    proc = subprocess.Popen(['python', DAEMON_PATH + DAEMON_NAME + '.py'], cwd=DAEMON_PATH, shell=True, stdout=DEVNULL, stderr=DEVNULL)
    print(f'Daemon process started on localhost with pid={proc.pid}\n')

if __name__ == "__main__":

    global cwd
    cwd = os.path.dirname(sys.argv[0])
    DAEMON_PATH = os.path.abspath(cwd) + '/' + DAEMON_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument('--dport', default=DAEMON_PORT, type=int, help="<optional> daemon port")
    args = parser.parse_args()

    if not checkDaemonRunning():
        print('Daemon process not found. Attempting to start...\n')
        startDaemon()

    print(f'Attempting to connect daemon on port {args.dport}...\n')