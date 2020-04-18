from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile
from .validate import validate_password,validate_username,getFileSize


class UserSimpleSerializer(serializers.HyperlinkedModelSerializer):
    '''
    处理用户列表展示 api/user GET
    '''

    class Meta:
        model = UserProfile
        fields = ('url', 'id', 'urltoken', 'nickname', 'username', 'avatar','is_staff')
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'urltoken'},
        }


class UserSerializer(serializers.ModelSerializer):
    '''
    处理用户详情展示  api/user/urltoken  GET
    '''
    user_gender = serializers.CharField(source='get_gender_display')
    class Meta:
        model = UserProfile
        exclude = ('password', 'groups', 'user_permissions')


class UserUpdateSerializer(serializers.ModelSerializer):
    '''
    处理用户详情展示  api/user/urltoken  GET
    '''

    class Meta:
        model = UserProfile
        fields = ('nickname', 'avatar', 'headline', 'birth_date', 'gender', 'email', 'desc', 'address')


class UserRegSerializer(serializers.ModelSerializer):
    '''
    处理用户注册  api/user/       POST
    '''
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False, max_length=24,
                                     validators=[validate_username,UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])
    password = serializers.CharField(style={'input_type': 'password'}, help_text="密码", label="密码",
                                     write_only=True, min_length=6, max_length=24,validators=[validate_password])

    class Meta:
        model = UserProfile
        fields = ('username', 'password',)


    def create(self, validated_data):
        user = UserProfile(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField( required=True )
    class Meta:
        model = UserProfile
        fields = ('avatar',)

    def validate_avatar(self,avatar):
        if not getFileSize(avatar.size,512000):
            raise serializers.ValidationError('最大图像文件大小500k')
        return avatar