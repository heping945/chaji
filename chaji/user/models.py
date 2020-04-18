import uuid
import os
from unidecode import unidecode

from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 定义用户头像上传路径
# 为用户创建单独文件夹，头像放在内置的avatar文件里，其他文档放在document里
def user_directory_path(instance, filename):
    # 取上传文件类型
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'file'
    if ext.lower() in ['jpg', 'png', 'gif' ,'jpeg']:
        sub_folder = 'avatar'
    if ext.lower() in ['pdf', 'docx']:
        sub_folder = 'document'
    return os.path.join('avatars',instance.username, filename)




class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        (1, '男'),
        (0, '女'),
        (-1, '未知')
    )
    id = models.UUIDField(primary_key=True,auto_created=True,editable=False,default=uuid.uuid4)
    nickname = models.CharField('昵称', max_length=32, null=True, blank=True)
    gender = models.IntegerField(
        '性别',
        choices=GENDER_CHOICES,
        default=-1)
    address = models.CharField('居住地', max_length=100, null=True, blank=True)
    birth_date = models.DateField('生日', null=True, blank=True)
    email = models.EmailField('邮箱', null=True, blank=True,unique=True)
    phone = models.CharField('手机', max_length=11, null=True, blank=True,unique=True)
    desc = models.CharField('个人描述', null=True, blank=True, max_length=250)
    avatar = models.ImageField(
        '头像',
        upload_to=user_directory_path,
        default='/avatars/default.png',blank=True)
    headline = models.CharField('简介',max_length=30,null=True,blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True,)
    mod_date = models.DateTimeField('上次更新时间', auto_now=True)
    urltoken = models.SlugField('urltoken', max_length=60, blank=True)

    def __str__(self):
        return self.username or self.nickname

    class Meta:
        verbose_name = '用户账户'
        verbose_name_plural = verbose_name
        ordering =['create_time']

    def save(self, *args, **kwargs):
        if not self.id or not self.urltoken:
            # Newly created object, so set slug
            self.urltoken = slugify(unidecode(self.username))

        super().save(*args, **kwargs)