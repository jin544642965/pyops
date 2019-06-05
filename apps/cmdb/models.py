from django.db import models

# Create your models here.

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"网络设备"),
    (str(5), u"安全设备"),
    (str(6), u"其他")
    )


class Idc(models.Model):
    name = models.CharField(u"机房名称", max_length=255, unique=True)
    address = models.CharField(u"机房地址", max_length=100, blank=True)
    tel = models.CharField(u"机房电话", max_length=30, blank=True)
    contact = models.CharField(u"客户经理", max_length=30, blank=True)
    contact_phone = models.CharField(u"移动电话", max_length=30, blank=True)
    ip_range = models.CharField(u"IP范围", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    # 返回一个用户可读对象
    def __str__(self):
        return self.name

    # 内嵌类定义元数据，verbose_name给模型取一个更可读的名字
    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    ip = models.GenericIPAddressField(u"管理IP", max_length=15)
    # account = models.ForeignKey(AuthInfo, verbose_name=u"账号信息", on_delete=models.SET_NULL, null=True, blank=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, blank=True)
    vendor = models.CharField(u"设备厂商", max_length=50, blank=True)
    cpu_model = models.CharField(u"CPU型号", max_length=100, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=255, blank=True)
    position = models.CharField(u"所在位置", max_length=100, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.hostname


class HostGroup(models.Model):
    name = models.CharField(u"服务器组名", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, blank=True)

    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"所在服务器"
    )

    def __str__(self):
        return self.name

