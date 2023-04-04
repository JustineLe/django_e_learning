from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data')
        # Fix the passwords of fixtures
        user = User.objects.first()
        if user:
            user.set_password("123456")
            user.save()
