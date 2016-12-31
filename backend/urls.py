from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token
from authentication.views import UserViewSet, get_token
from caves.views import CaveView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', get_token),
    url(r'^api/caves/$', CaveView.as_view()),
    url(r'^api/caves/(?P<id>[0-9]+)/$', CaveView.as_view()),
    url(r'^api-token-verify/', verify_jwt_token),
]
