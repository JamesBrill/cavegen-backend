from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
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

    def post(self, request, format=None):
        serializer = CaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
