from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,"删除"),
    )

    name = models.CharField(max_length=50,verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name="状态")
    is_nav = models.BooleanField(default=False,verbose_name="是否为导航")
    owner = models.ForeignKey(User,verbose_name="作者",on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,"删除"),
    )
    name = models.CharField(max_length=50,verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name="状态")
    owner = models.ForeignKey(User,verbose_name="作者",on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,"删除"),
        (STATUS_DRAFT,"草稿"),
    )

    title = models.CharField(max_length=255,verbose_name="标题")
    #blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
    desc = models.CharField(max_length=1024,blank=True,verbose_name="摘要")
    #help_text 在该 field 被渲染成 form 是显示帮助信息
    content = models.TextField(verbose_name="正文",help_text=("正文必须为MarkDown格式"))
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,verbose_name="状态")
    category = models.ForeignKey(Category,verbose_name="分类",on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag,verbose_name="标签")
    owner = models.ForeignKey(User,verbose_name="作者",on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "文章"  #配置展示名
        ordering = ['-id'] #根据ID进行降序排列

    def __str__(self):
        return self.title
