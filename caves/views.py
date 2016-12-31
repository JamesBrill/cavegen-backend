from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Cave
from .serializers import CaveSerializer
from django.http import StreamingHttpResponse
import os

class CaveView(APIView):
    def get_object(self, id):
        try:
            return Cave.objects.get(id=id)
        except Cave.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        cave = self.get_object(id)
        if request.user.username != cave.author.username:
            return Response({'error': 'You are not authorized to access this cave.'}, status=status.HTTP_403_FORBIDDEN)
        file = open('temp.txt', 'w')
        file.write(cave.text)
        file.close()
        file = open('temp.txt', 'r').read()
        response = StreamingHttpResponse(file)
        response['Content-Type'] = 'text/plain; charset=utf8'
        os.remove('temp.txt')
        return response

    def post(self, request, format=None):
        data = request.data
        data['author'] = request.user.id
        serializer = CaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
