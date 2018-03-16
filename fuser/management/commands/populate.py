from django.core.management.base import BaseCommand

from alerts.models import Alert, AlertHelper
from clients.models import Client
from hosts.models import Host

from django.contrib.auth import get_user_model

class Command(BaseCommand):
    args = ''
    help = 'Populate Database'

    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--production',
            default=False,
            action='store_true',
            dest='production',            
            help='Create production users',
        )

        parser.add_argument(
            '--development',
            default=False,
            action='store_true',
            dest='development',            
            help='Create development users',
        )

    def handle(self, *args, **options):

        User = get_user_model()
        User.objects.create_superuser('admin@example.com', 'pass')





