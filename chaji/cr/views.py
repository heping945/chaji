from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from celery.result import AsyncResult

from .tasks import CRHandle
from utils.apiconfig import client

def validate_method(cls,method):
    return hasattr(cls,method)

LIMIT_IMAGE_SIZE = 1024*1024*5  # 最大图片尺寸

def limit_image_size(size,base=LIMIT_IMAGE_SIZE):
    return size < base


class CRAIViewset(viewsets.ViewSet):
    lookup_field = 'taskId'
    def create(self,*args,**kwargs):
        image = self.request.data.get('image')
        url = self.request.data.get('url')
        query_params = self.request.query_params
        handletype = query_params.get('type')       # 处理类型
        handlearg = query_params.get('arg','')         # 参数
        print(handlearg)
        if image and limit_image_size(image.size) or url:
            if validate_method(client,handletype):
                if url:
                    res = CRHandle.delay(handletype, url,handlearg )
                else:
                    content = image.read()
                    res = CRHandle.delay(handletype,content,handlearg)
                d = {
                    'msg': 'success',
                    'code': 1001,
                    'data': res.id
                }
                return Response(d,status=status.HTTP_201_CREATED)
        d = {
            'msg': 'failure',
            'code': 1004,
            'data': None
        }
        return Response(d)

    def retrieve(self,*args,**kwargs):
        taskId=kwargs.get('taskId',None)
        if taskId:
            res = AsyncResult(taskId)
            if res.successful():
                print(res.get())
                print('success')
            else:
                print('failure')
        d = {
            'msg':'success',
            'code':1001,
            'data':taskId

        }
        return Response(d)