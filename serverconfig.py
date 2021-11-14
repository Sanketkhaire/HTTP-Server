from configparser import  ConfigParser


config = ConfigParser()
config.read('server.conf')

#Port on which you want to run myHTTP server
PORT_NUMBER = int(config.get('SERVER','PORT'))

#Path where all the files exist . Also called as the server root
DOCUMENT_ROOT = config.get('SERVER','DOCUMENT-ROOT')

#Maximum number of connections to serve at a time (simultaneously)
MAX_CONNECTION = int(config.get('SERVER','MAX-CONNECTION'))

#Level of logging
LOG_LEVEL = config.get('LOGS','LOG-LEVEL')

#includes all logs when the error occurs and the reason
ERROR_LOG = config.get('LOGS','LOG-DIRECTORY') + config.get('LOGS','ERROR-LOGS')


#Includes all the data of every request
ACCESS_LOG = config.get('LOGS','LOG-DIRECTORY') + config.get('LOGS','ACCESS-LOGS')

