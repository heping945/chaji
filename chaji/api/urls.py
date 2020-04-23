from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token


from user.views import UserViewset, UserPasswordViewset,UserAvatarViewset,UserinfoViewset
from info.views import RequestInfoViewset

router = DefaultRouter()

router.register(r'users', UserViewset, base_name='user')
router.register(r'user', UserinfoViewset, base_name='userinfo')
router.register(r'userpwd',UserPasswordViewset,basename='userpwd')
router.register(r'avatar',UserAvatarViewset,basename='avatar')
router.register(r'reqinfo',RequestInfoViewset,basename='reqinfo')

urlpatterns = [
    url(r'^', include(router.urls)),
    # 登录接口
    url(r'^login/$', obtain_jwt_token),
    # jwt token刷新延长登录接口
    url(r'^refresh/$', refresh_jwt_token),
]
