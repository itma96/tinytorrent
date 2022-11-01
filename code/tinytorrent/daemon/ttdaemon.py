import string
import sys
import os
import argparse, configparser
import logging
import setproctitle
import traceback

from subprocess import DEVNULL


DAEMON_NAME = 'ttdaemon'
DAEMON_PORT = 6667
CONFIG_NAME = 'daemon.ini'
CONFIG_PATH = './'

LOGGER = None

def parseConfigFile(file: string) -> dict:
    global LOGGER, CONFIG_PATH, CONFIG_NAME, CWD, VERBOSE
    try:
        print('Reading config file\n')
        if file != CONFIG_NAME:
            f = open(args.config, "r")
        else:
            f = open(os.path.abspath(CWD) + '/' + CONFIG_PATH + CONFIG_NAME, "r")
        config = configparser.ConfigParser()
        config.read_file(f)

        # === Logging configuration ===

        logging_config = config['daemon.logging']

        if logging_config:
            print('Logging configuration found:\n')
            LOGGER = logging.getLogger(__name__)

            LOGGER.name = 'ttdaemon'

            # for verbose mode only
            if VERBOSE:
                ch = logging.StreamHandler()
                LOGGER.addHandler(ch)
                
            # set log level
            if 'loglevel' in logging_config:
                print(f'\tUsing log level: {logging_config["loglevel"]}\n')
                LOGGER.setLevel(logging[logging_config['loglevel']])
            else:
                print(f'\tUsing implicit log level: INFO\n')
                LOGGER.setLevel(logging.INFO)
            # set log file
            if 'logfile' in logging_config:
                print(f'\tUsing log file: {logging_config["logfile"]}\n')
                fh = logging.FileHandler(logging_config["logfile"])
                LOGGER.addHandler(fh)
            else:
                print(f'\tUsing implicit log file: {os.path.abspath(CWD) + "/" + DAEMON_NAME + ".log"}\n')
                fh = logging.FileHandler(os.path.abspath(CWD) + "/" + DAEMON_NAME + ".log")
                LOGGER.addHandler(fh)
            # set log format
            if 'format' in logging_config:
                print(f'\tUsing format: {logging_config["format"]}\n')
                format = logging_config["format"]
                formatter = logging.Formatter(format)
                for handler in LOGGER.handlers:
                    handler.setFormatter(formatter)
            else:
                print(f'\tUsing implicit format: {logging.BASIC_FORMAT}\n')
    except (IOError, configparser.Error):
        print('Unable to open/parse config file! Aborting...\n')
        traceback.print_exc()
        f.close()
        sys.exit(1)
    else:
        return config

def main(config):
    LOGGER.info('Starting message queue...')



if __name__ == "__main__":

    setproctitle.setproctitle(DAEMON_NAME)

    global CWD, VERBOSE 
    CWD = os.path.dirname(sys.argv[0])
    VERBOSE = False
    
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = open(os.devnull, 'w')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Turn on verbose mode.")
    parser.add_argument("--config", action='store', default=CONFIG_NAME, help="Path to config file.")
    args = parser.parse_args()

    if args.verbose:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        VERBOSE = True

    print('Daemon process starting...\n')
    cfg = parseConfigFile(args.config)
    LOGGER.info('Loaded configuration ')
    main(cfg)


