from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import Cave

class CaveSerializer(ModelSerializer):
    author_name = CharField(source='author.userprofile.display_name', read_only=True)
    class Meta:
        model = Cave
        fields = ('id', 'name', 'uuid', 'text', 'author', 'is_public', 'date_created', 'author_name')
