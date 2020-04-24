import  random
import string
import os
import time

from django.conf import settings
from django.core.mail import send_mail
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chaji.settings")

app = Celery('tasks', broker='redis://127.0.0.1/7',backend='redis://127.0.0.1/8')



# 生成n位随机码
def generate_code(n=6):
    _str = string.ascii_letters+string.digits
    return ''.join(random.sample(_str,n))

@app.task(time_limit=10)
def send_email():
    code = generate_code()
    msg = f'''
                        <p>输入此段code:  <strong>{code}</strong></p>
                        <div>
                          确认code：<input type="text">
                        </div>
                        '''
    sendToEmail = ('602013597@qq.com',)
    title = 'hello world'
    content = '你好啊'
    res = send_mail(title, content, settings.DEFAULT_FROM_EMAIL,
                    sendToEmail, html_message=msg)


@app.task
def add(x,y):
    time.sleep(3)
    print(x+y)
    return x+y