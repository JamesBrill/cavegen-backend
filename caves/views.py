from rest_framework.viewsets import ModelViewSet
from .models import Cave
from .serializers import CaveSerializer

class CaveViewSet(ModelViewSet):
    queryset = Cave.objects.all()
    serializer_class = CaveSerializer
