from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token
from authentication.views import UserViewSet, get_token
from caves.views import CaveView, get_my_caves

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', get_token),
    url(r'^api/caves/$', CaveView.as_view()),
    url(r'^api/caves/(?P<uuid>[0-9a-z\-]+)/$', CaveView.as_view()),
    url(r'^api/my-caves/$', get_my_caves),
    url(r'^api-token-verify/', verify_jwt_token),
]
