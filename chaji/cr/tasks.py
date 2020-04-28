from celery_app import app
from utils.apiconfig import client


@app.task
def crhandle(method,imageContent,*args):
    func = getattr(client, method)
    res = func(imageContent,*args,)
    return res