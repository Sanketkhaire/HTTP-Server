from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.optionxform = str

config['SERVER'] = {
    'DOCUMENT-ROOT': str(Path().resolve()) + '/var/www/html2',
    'MAX-CONNECTION': 30,
    'PORT': 12008,
    'KEEP-ALIVE': 'On',
    'TIMEOUT': 300
}

config['LOGS'] = {
    'LOG-LEVEL': 'DEBUG',
    'LOG-DIRECTORY': str(Path().resolve()) + '/var/log/myhttp/',
    'ERROR-LOGS': 'error.log',
    'ACCESS-LOGS': 'access.log',
    'LOG-FORMAT': 'Client-IP [Timestamp] "Request" Status-code Request-size "Referer" "User-agent"',
    'COOKIE-FILE': 'cookie.txt',
}

cf = open("server.conf", 'w')

config.write(cf)
cf.close()