# management/commands/index_profiles.py

from django.core.management.base import BaseCommand
from myapp.documents import UserProfileDocument
from myapp.models import UserProfile
from elasticsearch import ElasticsearchException

class Command(BaseCommand):
    help = 'Indexes user profiles'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Index a specific user by username')
        parser.add_argument('--reindex', action='store_true', help='Reindex all profiles')

    def handle(self, *args, **options):
        if options['username']:
            try:
                profile = UserProfile.objects.get(username=options['username'])
                UserProfileDocument().update(profile)
                self.stdout.write(self.style.SUCCESS(f'Successfully indexed profile for user: {profile.username}'))
            except UserProfile.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with username {options["username"]} does not exist'))
            except ElasticsearchException as e:
                self.stdout.write(self.style.ERROR(f'Error indexing profile for user: {profile.username} - {str(e)}'))
        elif options['reindex']:
            profiles = UserProfile.objects.all()
            for profile in profiles:
                try:
                    UserProfileDocument().update(profile)
                    self.stdout.write(self.style.SUCCESS(f'Successfully indexed profile for user: {profile.username}'))
                except ElasticsearchException as e:
                    self.stdout.write(self.style.ERROR(f'Error indexing profile for user: {profile.username} - {str(e)}'))
        else:
            self.stdout.write(self.style.ERROR('Please provide a username or use the --reindex flag'))

