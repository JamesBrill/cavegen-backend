from django.conf import settings
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import UserProxy
from .serializers import UserSerializer, UserProfileSerializer

import json
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProxy.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request):
        data = request.data
        query_set = UserProxy.objects.filter(email=data['email'])

        if query_set.count() == 0:
            profile = data.pop('userprofile')
            user = UserProxy.objects.create(validated_data=data, profile=profile)
            UserProxy.objects.create_colleagues(user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'email exists'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_token(request):
    code = request.query_params.get('code')
    json_header = {'content-type': 'application/json'}
    has_error = request.query_params.get('error', False)

    if has_error:
        next_url = settings.EXTERNAL_URLS['BASE']
        headers = {'Location': next_url, 'content-type': 'text/plain'}
        return Response('redirecting to ' + next_url, headers=headers, status=status.HTTP_302_FOUND)

    token_url = "https://{domain}/oauth/token".format(domain='cavegen-app.auth0.com')

    uri = 'http://' + request.get_host()

    token_payload = {
        'audience': 'https://cavegen-app.auth0.com/api/v2/',
        'client_id': settings.JWT_AUTH['JWT_AUDIENCE'],
        'client_secret': settings.JWT_AUTH['JWT_ENCODED_SECRET_KEY'],
        'redirect_uri': uri,
        'code': code,
        'grant_type': 'authorization_code'
    }
    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    if 'access_token' not in token_info:
        next_url = settings.EXTERNAL_URLS['BASE']
        text_headers = {'Location': next_url, 'content-type': 'text/plain'}
        return Response('redirecting to ' + next_url, headers=text_headers, status=status.HTTP_302_FOUND)

    user_url = 'https://{domain}/userinfo?access_token={access_token}' \
        .format(domain='cavegen-app.auth0.com', access_token=token_info['access_token'])
    user_info = requests.get(user_url).json()

    v2_url = 'https://{domain}/api/v2/users/{user_id}' \
        .format(domain='cavegen-app.auth0.com', user_id=user_info['user_id'])

    json_header['Authorization'] = 'Bearer ' + token_info['id_token']
    v2_info = requests.get(v2_url, headers=json_header).json()
    data = {
        'userprofile': {
            'picture': v2_info['picture']
        }
    }

    if 'email' in v2_info:
        data['email'] = v2_info['email']
    else:
        # This is bad, but gets us a username for JWT auth for now
        data['email'] = v2_info['user_id']

    if 'given_name' in v2_info:
        data['first_name'] = v2_info['given_name']
    elif 'first_name' in v2_info:
        data['first_name'] = v2_info['first_name']

    if 'family_name' in v2_info:
        data['last_name'] = v2_info['family_name']
    elif 'last_name' in v2_info:
        data['last_name'] = v2_info['last_name']

    if 'name' in v2_info:
        data['userprofile']['display_name'] = v2_info['name']
    elif 'nickname' in v2_info:
        data['userprofile']['display_name'] = v2_info['nickname']
    else:
        data['userprofile']['display_name'] = 'anonymous'

    query_set = UserProxy.objects.filter(email=data['email'])
    if query_set.count() == 0:
        profile = data.pop('userprofile')
        user = UserProxy.objects.create(validated_data=data, profile=profile)
        user.userprofile.save()

    redirectUrl = settings.EXTERNAL_URLS['BASE_WITH_TOKEN']
    formattedRedirectUrl = redirectUrl.format(id_token=token_info['id_token'])
    headers = {'Location': formattedRedirectUrl, 'content-type': 'text/plain'}
    return Response('redirecting to ' + formattedRedirectUrl, headers=headers, status=status.HTTP_302_FOUND)

class UserProfileView(APIView):
    def get_object(self, username):
        try:
            return UserProxy.objects.get(username=username)
        except UserProxy.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.username)
        serializer = UserProfileSerializer(user.userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = self.get_object(request.user.username)
        userprofile = user.userprofile
        serializer = UserProfileSerializer(userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
