import logging
from django.http import HttpResponse
from logger.config import DJANGO_DB_LOGGER_ENABLE_FORMATTER


db_default_formatter = logging.Formatter()
logger = logging.getLogger('db_logger') # name should be same as the name used in logging.handlers in settings.py

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import StatusLog
        print('record', record)
        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace
        }

        StatusLog.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
        
def __gen_500_errors(request):
  try:
    1/0
  except Exception as e:
    logger.exception(e)

  return HttpResponse('Hello 500!')

def test_logger(**kwargs):
  try:
    if kwargs.get('debug'):
      logger.debug('Debug log')
    if kwargs.get('info'):
      logger.info('Info log')
    if kwargs.get('warning'):
      logger.warning('Warning log')
    if kwargs.get('error'):
      logger.error('Error log')
    if kwargs.get('fatal'):
      logger.fatal('Fatal log')
    if kwargs.get('exception'):
      try:
        1/0
      except Exception as e:
        logger.exception(e)
    if kwargs.get('all'):
      logger.debug('Debug log')
      logger.info('Info log')
      logger.warning('Warning log')
      logger.error('Error log')
      logger.fatal('Fatal log')
      try:
        1/0
      except Exception as e:
        logger.exception(e)
    return
  except Exception as e:
    logger.exception(e)
    return