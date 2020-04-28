import random
import string

from django.core.mail import send_mail

from celery_app import app
from django.conf import settings


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
    send_mail(title, content, settings.DEFAULT_FROM_EMAIL,
                    sendToEmail, html_message=msg)
