from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Cave

class CaveSerializer(ModelSerializer):
    class Meta:
        model = Cave
        fields = ('id', 'uuid', 'text', 'author')
