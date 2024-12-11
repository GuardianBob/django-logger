from __future__ import unicode_literals
import logging

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from logger.config import DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
from .models import StatusLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('app', 'file', 'colored_msg', 'create_datetime', 'traceback', )
    list_display_links = ('colored_msg',)
    list_filter = ('level', 'app', 'file',)
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
    ordering = ('-create_datetime',)  # Add this line to enable sorting by create_datetime

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING]:
            color = 'orange'
        elif instance.level in [logging.DEBUG]:
            color = '#0066d3'
        elif instance.level in [logging.ERROR]:
            color = '#ea2e00'
        else:
            color = '#a80000'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    colored_msg.short_description = 'Message'

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return timezone.localtime(instance.create_datetime).strftime('%Y-%m-%d %X')

    create_datetime_format.short_description = 'Created at'


admin.site.register(StatusLog, StatusLogAdmin)