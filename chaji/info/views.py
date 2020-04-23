from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .utils import ADDREQ


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