from django.apps import AppConfig
import django_heroku


class T3Config(AppConfig):
    name = 't3'


django_heroku.settings(locals())
