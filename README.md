# Django DB Logger


## Adding the logger to your project

- In your **settings.py** file add `'logger,'` to `INSTALLED_APPS`.
- If you have a `LOGGING` section add the following, otherwise create a `LOGGING` section:
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'logger.db_logger.DatabaseLogHandler'
        },
    },
    # Add a logger for each app that you want to log to the database
    'loggers': {
        'logger': { # use app name here to specify which app is being logged
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
    },
}
```
- Under `loggers` make sure to add a *logger* for each app in your project that you want to add database logging to
- Make sure to set the name of the `logger` to the name of the app the logger is being added to.
  - Ex:
  > If you have an app named "calendar", add a logger under `loggers` and name it "calendar"

- Make sure to run `python manage.py makemigrations` and `python manage.py migrate` to add the necessary table to your database.

## Testing the logger

There are built in tests that can be run for each type of log once you've added the Django Database Logger to your project.
The command `python manage.py logger test_logger` can be run to create a test log entry in your project's database for each log type.
The following arguments can be added to test individual log types:
```
--debug       #Test debug log.
--info        #Test info log.
--warning     #Test warning log.
--error       #Test error log.
--critical    #Test critical log.
--exception   #Test exception log.
--all         #Test all log levels.
```

## Customization

Log message colors displayed in the Django admin UI can be changed in the `admin.py` file along with log filters. 