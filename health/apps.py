from django.apps import AppConfig
from mongoengine import connect, disconnect
import os


class HealthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health'

    def ready(self):
        disconnect()  # Disconnect if already connected
        connect(
            db=os.getenv('MONGO_DB_NAME'),
            host=os.getenv('MONGO_HOST'),
            username=os.getenv('MONGO_USERNAME'),
            password=os.getenv('MONGO_PASSWORD')
        )
