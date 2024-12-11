import logging, inspect
from django.http import HttpResponse
from logger.db_logger import DatabaseLogging

# logger = logging.getLogger(__name__) # name should be same as the name used in logging.handlers in settings.py
logger = DatabaseLogging(__name__)
# logger = DatabaseLogging('logger')

def __gen_500_errors(request):
  try:
    1/0
  except Exception as e:
    logger.exception(e)

  return HttpResponse('Hello 500!')

def log_with_trace(level, message):
  frame = inspect.currentframe().f_back
  trace_message = f"Function: {frame.f_code.co_name}, Line: {frame.f_lineno}"
  exc_info = (None, None, None, trace_message)
  
  if level == 'debug':
    logger.debug(message, exc_info=exc_info)
  elif level == 'info':
    logger.info(message, exc_info=exc_info)
  elif level == 'warning':
    logger.warning(message, exc_info=exc_info)

def test_all():
  logger.debug('Debug testing log entry')
  logger.info('Info testing log entry')
  logger.warning('Warning testing log entry')
  logger.error('Error testing log entry')
  logger.critical('Critical testing log entry')
  try:
    1/0
  except Exception as e:
    logger.exception(e)
  return

def test_logger(**kwargs):
  try:
    if kwargs.get('debug'):
      log_with_trace('debug', 'Debug testing log entry')
    if kwargs.get('info'):
      logger.info('Info testing log entry')
    if kwargs.get('warning'):
      logger.warning('Warning testing log entry')
    if kwargs.get('error'):
      logger.error('Error testing log entry')
    if kwargs.get('critical'):
      logger.critical('Critical testing log entry')
    if kwargs.get('exception'):
      try:
        1/0
      except Exception as e:
        logger.exception(e)
    if kwargs.get('all'):
      test_all()
    else:
      test_all()
    return
  except Exception as e:
    logger.exception(e)
    return