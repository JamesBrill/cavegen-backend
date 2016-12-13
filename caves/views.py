from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cave
from .serializers import CaveSerializer

class CaveView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get_object(self, id):
        try:
            return Cave.objects.get(id=id)
        except Cave.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        cave = self.get_object(id)
        serializer = CaveSerializer(cave)
        return Response(serializer.data)
