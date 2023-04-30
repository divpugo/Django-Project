from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates the leads group if it does not already exist.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='leads')

        if created:
            self.stdout.write(self.style.SUCCESS('Leads group was created.'))
        else:
            self.stdout.write(self.style.WARNING('Leads group already exists.'))
