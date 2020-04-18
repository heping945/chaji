from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from .permissions import IsCurUserOrReadOnly,IsCurUser
from rest_framework.mixins import UpdateModelMixin

from .validate import validpassword
from .serializers import UserSerializer,UserSimpleSerializer,UserRegSerializer,UserUpdateSerializer,UserAvatarSerializer
from .models import UserProfile

# 一个需要登录用户获得当前用户简略信息的视图
class UserinfoViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    queryset = UserProfile.objects.all()
    lookup_field = 'urltoken'
    ordering_fields = ('create_time',)
    serializer_class = UserSimpleSerializer
    permission_classes = (IsCurUser,)



class UserViewset(viewsets.ModelViewSet):
    '''
    处理api/userprofile
    '''
    queryset = UserProfile.objects.all()
    lookup_field = 'urltoken'
    ordering_fields = ('create_time',)
    authentication_classes = []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializer
        elif self.action == 'list':
            return  UserSimpleSerializer
        elif self.action == 'create':
            return  UserRegSerializer
        return UserUpdateSerializer



class UserPasswordViewset(viewsets.ViewSet):
    permission_classes = (IsCurUserOrReadOnly,)
    lookup_field = 'username'
    def partial_update(self, request,username):
        data = {}
        rpwd = request.data.get('password',None)
        npwd = request.data.get('password2',None)
        if all([username,rpwd,npwd]) and rpwd!=npwd:
            user = UserProfile.objects.filter(username=username).first()
            self.check_object_permissions(self.request, user)       # 权限验证
            if user:
                if user.check_password(rpwd):
                    if validpassword(npwd):
                        user.set_password(npwd)
                        user.save(update_fields=["password"])
                        data['msg']='scuusss'
                        data['code']=666
                        return Response(data)
        data['msg']='bad request'
        data['code']=999
        return Response(data)



class UserAvatarViewset(viewsets.GenericViewSet,UpdateModelMixin):
    lookup_field = 'username'
    permission_classes = (IsCurUserOrReadOnly,)
    serializer_class = UserAvatarSerializer
    queryset = UserProfile.objects.all()