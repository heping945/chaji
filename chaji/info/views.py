from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection
from celery.result import AsyncResult

from .utils import ADDREQ,ShortUrl
from .tasks import send_email
from utils.func import IpRecord
from celery_app.tasks import add

ip = get_redis_connection('chaji')
dwz = get_redis_connection('chaji')

s = ShortUrl(dwz)





class RequestInfoViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        data = {}
        print(request)
        data['msg']='success'
        data['code']=1000
        d = request.META
        res = {}
        for k,v in d.items():
            if k.startswith('HTTP') or k in ADDREQ:
                res[k] = v
        data['data'] =res
        return Response(data)

class GetIPViewset(viewsets.ViewSet):
    def list(self, request, **kwargs):
        iplog = IpRecord(ip)
        iplist = iplog.get()
        if iplist:
            data = {
                'result':iplist,
                'msg':'success',
                'code':'1000'
            }
        else:
            data = {
                'result': [],
                'msg': 'failure no data',
                'code': '1004'
            }
        return Response(data)

class DwzViewset(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        long_url = request.data.get('url')
        ret = {}
        if long_url:
            short_url = s.shorten(long_url, 10000000)
            ret['data'] = short_url
            ret['code'] = 1
            ret['msg'] = 'success'
        else:
            ret = {
                'code': 0,
                'msg': '参数错误'
            }
        return Response(ret)

    def retrieve(self, request, *args, **kwargs):
        show_id = kwargs.get('pk')
        ret = {'code': 2, 'data': None,'msg':'未查询到信息'}
        try:
            res = s.restore(show_id)
            if res:
                ret = {'data': res, 'code': 1, 'msg': 'success'}
        except Exception as e:
            ret = {'code': 0, 'msg': '参数错误'}

        return Response(ret)



class CeleryViewset(viewsets.ViewSet):
    def list(self, request, **kwargs):
        res_id = send_email.delay()
        print(res_id)
        res = AsyncResult('2bc77cb5-53f2-4c7e-b77e-6f5e82575ddb')
        if res_id.successful():
            print(res.get())
        else:
            print('failure')
        return Response('ok')
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        res_id=add.delay(1,2)
        d = {
            'msg':'success',
            'pk':pk,
            # 'res_id':res_id,
        }
        return Response(d)

