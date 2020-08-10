from django.db import models

# Create your models here.

class Certificate(models.Model):
    certificate_name = models.CharField("认证名称", max_length=255, unique=True)
    username = models.CharField("用户名", max_length=100, blank=True)
    password = models.CharField("密码", max_length=30, blank=True)
    port = models.CharField("端口", max_length=5, blank=True)
    private_key = models.TextField("密钥",max_length=16000, blank=True)
    remask = models.TextField("备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.certificate_name