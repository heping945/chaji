from rest_framework import permissions


class IsCurUserOrReadOnly(permissions.BasePermission):
    """
    只允许作者修改但允许所有人读的权限设置
    """

    def has_object_permission(self, request, view, obj):
        # 所有用户都允许读取,所以安全的http方法会直接放行
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限需要作者本人
        # print(obj,'obj')
        # print(request.user,'requser')
        return obj == request.user

class IsCurUser(permissions.BasePermission):
    """
    只允许当前user获取的权限设置
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user