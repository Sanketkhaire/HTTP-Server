import logging
from logging import Handler
from serverconfig import LOG_LEVEL,DOCUMENT_ROOT

logger = logging.getLogger('server')

if(LOG_LEVEL == 'DEBUG'):
    logger.setLevel(logging.DEBUG)
elif(LOG_LEVEL == 'ERROR'):
    logger.setLevel(logging.ERROR)
elif(LOG_LEVEL == 'SERVER'):
    logger.setLevel(logging.CRITICAL)

formatter = logging.Formatter('[%(asctime)s.%(msecs)05d] [pid %(process)s:tid %(thread)s] %(message)s',"%a %b %d %Y %H:%M:%S")
file_handler = logging.FileHandler('error.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)