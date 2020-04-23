from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

from utils.func import IpRecord
iplog = get_redis_connection('chaji')

class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    def process_request(self, request):
        instance = IpRecord(iplog)
        ip = request.META.get('HTTP_X_REAL_IP', '')
        if ip:
            instance.set(ip)
