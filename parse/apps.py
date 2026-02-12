from django.apps import AppConfig


class ParseConfig(AppConfig):
    name = 'parse'


    def ready(self):
        from .scheduler import start
        start()