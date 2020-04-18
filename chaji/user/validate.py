import re

from rest_framework.exceptions import ValidationError


def validate_mobile(value):
    r = re.compile(
        r'^(((13[0-9]{1})|(15[0-9]{1})|(16[0-9]{1})|(17[3-8]{1})|(18[0-9]{1})|(19[0-9]{1})|(14[5-7]{1}))+\d{8})$')
    if not r.match(str(value)):
        raise ValidationError('手机号不合法')


def validate_password(value):
    r = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$")
    if not r.match(value):
        raise ValidationError('密码需要包括字母和数字，6-20字符')

def validpassword(value):
    r = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$")
    return r.match(value)

def validate_username(value):
    r = re.compile(r'^[a-zA-Z0-9_-]{2,24}$')
    if not r.match(value):
        raise ValidationError('用户名不能有特殊字符，2-16个字符')

# 限制文件大小
def getFileSize(size,limit=5242880):
    if size < limit:
        return True
    return False
