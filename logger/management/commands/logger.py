from django.core.management.base import BaseCommand
from logger import views
import argparse
import os

class Command(BaseCommand):
  help = 'Calls functions for KDS from the commmand line based on provided prameters.'
  
  parser = argparse.ArgumentParser(description="Process some parameters.")

  def add_arguments(self, parser):
    parser.add_argument('function_name', type=str, help='The name of the function to call.')
    parser.add_argument('--debug', action='store_true', help='Test debug log.')
    parser.add_argument('--info', action='store_true', help='Test info log.')
    parser.add_argument('--warning', action='store_true', help='Test warning log.')
    parser.add_argument('--error', action='store_true', help='Test error log.')
    parser.add_argument('--fatal', action='store_true', help='Test fatal log.')
    parser.add_argument('--exception', action='store_true', help='Test exception log.')
    parser.add_argument('--all', action='store_true', help='Test all log levels.')

  def handle(self, *args, **options):
    function_name = options.pop('function_name', None)
    try:
      run_function = getattr(views, function_name)
    except AttributeError:
      self.stdout.write(self.style.ERROR(f'Function "{function_name}" not found'))
    run_function(**options)
    self.stdout.write(self.style.SUCCESS(f'Successfully ran {function_name}'))