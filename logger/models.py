import logging
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
# class Log(models.Model):
#   type = models.CharField(max_length=255)
#   app_name = models.CharField(max_length=255)
#   file_path = models.CharField(max_length=255, null=True, blank=True)
#   line_number = models.IntegerField(null=True, blank=True)
#   message = models.TextField()
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)
  
#   def __str__(self):
#     return self.log


LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.CRITICAL, _('Critical')),
)

class StatusLog(models.Model):
    app = models.CharField(max_length=100)
    file = models.CharField(max_length=100, blank=True, null=True)
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField()
    trace = models.TextField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return self.msg

    class Meta:
        indexes = [
            models.Index(fields=['create_datetime']),
        ]
        ordering = ('-create_datetime',)
        verbose_name_plural = verbose_name = 'System Logs'