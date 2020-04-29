from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from celery.result import AsyncResult

from .tasks import crhandle
from utils.apiconfig import client

def validate_method(cls,method):
    return hasattr(cls,method)

LIMIT_IMAGE_SIZE = 1024*1024*5  # 最大图片尺寸
DEFAULT_IMAGE_MODE = 'basicGeneral'

def limit_image_size(size,base=LIMIT_IMAGE_SIZE):
    return size < base


class CRAIViewset(viewsets.ViewSet):
    lookup_field = 'taskId'
    def create(self,*args,**kwargs):
        image = self.request.data.get('image')
        url = self.request.data.get('url')
        print(image,url)
        query_params = self.request.query_params
        print(query_params)
        handletype = query_params.get('type')                   # 处理类型
        handlearg = query_params.get('arg',)                    # 参数
        handletype = handletype or DEFAULT_IMAGE_MODE           # 如果前端传入了空值就设置默认mode
        if image and limit_image_size(image.size) or url:
            if validate_method(client,handletype):
                if url:
                    res = crhandle.delay(handletype, url,handlearg )
                else:
                    content = image.read()
                    res = crhandle.delay(handletype,content,handlearg)
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
                data = res.get()
                d = {
                    'msg': 'success',
                    'code': 1001,
                    'data': data
                }
            else:
                d = {
                    'msg':'failure',
                    'code':1004,
                    'data':None
                }
        return Response(d)