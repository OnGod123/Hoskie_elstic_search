

from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from .models import UserProfile

user_index = Index('users')

@registry.register_document
class UserProfileDocument(Document):
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = UserProfile
        fields = [
            'username',
            'name',
            'email',
        ]

