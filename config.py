import logging
from logging.handlers import TimedRotatingFileHandler
from environment import *
bind = "127.0.0.1:8000" if runningMode=="deploy_" else "127.0.0.1:8001"
workers = 1

loglevel=logLevelStringLower
errorlog=runningMode+"gunicorn_error.log"
errorHandler = TimedRotatingFileHandler(errorlog, when='midnight', backupCount=0)
errorFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
errorHandler.setFormatter(errorFormatter)
errorLogger = logging.getLogger('gunicorn.error')
errorLogger.setLevel(logLevelStringUpper)
errorLogger.handlers = [errorHandler]

accesslog=runningMode+"gunicorn_access.log"
accessHandler = TimedRotatingFileHandler(accesslog, when='midnight', backupCount=0)
accessFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
accessHandler.setFormatter(accessFormatter)
accessLogger = logging.getLogger('gunicorn.access')
accessLogger.handlers = [accessHandler]
