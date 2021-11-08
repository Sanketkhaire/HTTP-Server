from configparser import  ConfigParser


config = ConfigParser()
config.read('server.conf')

DOCUMENT_ROOT = config.get('SERVER','DOCUMENT-ROOT')


MAX_CONNECTION = int(config.get('SERVER','MAX-CONNECTION'))

LOG_LEVEL = config.get('LOGS','LOG-LEVEL')

ERROR_LOG = config.get('LOGS','LOG-DIRECTORY') + config.get('LOGS','ERROR-LOGS')

ACCESS_LOG = config.get('LOGS','LOG-DIRECTORY') + config.get('LOGS','ACCESS-LOGS')

