import logging, inspect, os
from django.http import HttpResponse
from logger.config import DJANGO_DB_LOGGER_ENABLE_FORMATTER
from django.utils import timezone
import datetime


db_default_formatter = logging.Formatter()

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import StatusLog
        # print('record', record)
        trace = None

        if record.exc_info:
            if isinstance(record.exc_info, tuple) and len(record.exc_info) == 4:
                trace = record.exc_info[3]
            else:
                trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()
        
        if '.' in record.name:
            app_info = record.name.split('.')
            app_name = app_info[0]
            file_name = app_info[1]
            # print(f'app: {app_info[0]}, file: {app_info[1]}')
        else: 
            app_name = record.name
            file_name = None

        kwargs = {
            'app': app_name,
            'file': file_name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace
        }

        StatusLog.objects.create(**kwargs)
        self.purge_old_logs()

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
        
    def purge_old_logs(self):
        from .models import StatusLog
        cutoff_date = timezone.now() - datetime.timedelta(days=30)
        old_logs = StatusLog.objects.filter(create_datetime__lt=cutoff_date)
        old_logs.delete()

class DatabaseLogging:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def _log(self, level, message):
        frame = inspect.currentframe().f_back.f_back
        file_path = frame.f_code.co_filename
        app_name = os.path.basename(os.path.dirname(file_path))
        trace_message = f"Function: {frame.f_code.co_name}, Line: {frame.f_lineno}, File Path: {file_path}"
        exc_info = (None, None, None, trace_message)
        
        if level == 'debug':
            self.logger.debug(message, exc_info=exc_info)
        elif level == 'info':
            self.logger.info(message, exc_info=exc_info)
        elif level == 'warning':
            self.logger.warning(message, exc_info=exc_info)
        elif level == 'error':
            self.logger.error(message, exc_info=exc_info)
        elif level == 'critical':
            self.logger.critical(message, exc_info=exc_info)

    def debug(self, message):
        self._log('debug', message)

    def info(self, message):
        self._log('info', message)

    def warning(self, message):
        self._log('warning', message)

    def error(self, message):
        self._log('error', message)
    
    def critical(self, message):
        self._log('critical', message)

    def exception(self, message):
        self.logger.exception(message)

    def __call__(self, message):
        self.debug(message)