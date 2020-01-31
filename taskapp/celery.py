
import os
from celery import Celery
from django.apps import AppConfig
print("Environ is...")
print((os.environ.get('DJANGO_SETTINGS_MODULE')))
if os.path.exists('config/settings/settings_local.py'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings_local')  # pragma: no cover
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olade.settings')

from django.conf import settings

app = Celery('olade',
             include=['taskapp.tasks'])


class CeleryConfig(AppConfig):
    name = 'taskapp'
    verbose_name = 'Celery Config'

    def ready(self):

        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
        app.conf.broker_url = settings.BROKER_URL
        print(app.conf.broker_url)
        app.conf.broker_transport_options = {'visibility_timeout': 3600}
        app.conf.broker_transport_options = {'fanout_patterns': True}
        app.conf.broker_transport_options = {'visibility_timeout': 43200}


if __name__ == '__main__':
    app.start()
