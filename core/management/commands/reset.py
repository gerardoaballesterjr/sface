from django.core.management import call_command
from django.core.management.base import BaseCommand
from core.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system('pyclean .')
        
        try:
            for root, _, files in os.walk('core/migrations'):
                for file in files:
                    if file != '__init__.py':
                        os.remove(os.path.join(root, file))
        except:
            pass

        try:
            os.remove('main.db')
        except:
            pass
        
        call_command('makemigrations')
        call_command('migrate')

        user = User(first_name='Gerardo', last_name='Ballester', username='admin', is_superuser=True)
        user.set_password('admin')
        user.save()

        os.system('pyclean .')