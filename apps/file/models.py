from django.db import models

# Create your models here.


class Folder(models.Model):
    name = models.CharField(verbose_name="名称", max_length=20)  # 名称
