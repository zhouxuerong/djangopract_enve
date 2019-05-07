from django.contrib import admin
from .models import Post,Category,Tag
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
from xadmin.layout import Row,Fieldset,Container
from xadmin.filters import manager,RelatedFieldListFilter
import xadmin

#对于一个页面内容完成两个关联模型的需求，使用inline admin方式
# 在分类也看中直接编辑文章
class PostInline:  #StackedInline样式不同
    form_layout = (
        Container(
            Row("title", "desc")
        )
    )
    extra = 1
    model = Post

@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','owner')
    #fields控制页面上的展示
    fields = ('name','status','is_nav')
    inlines = [PostInline,]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)

# 关联自定义站点
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title',"category","status","created_time",'owner','operator']
    list_display_links = []
    # 指定哪些字段不展示
    exclude = ('owner',)

    list_filter = ['category', ]
    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True
    #fieldsets控制页面的布局
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        )
    )
    # classes 给配置板块加上css属性
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    # fields = (('category','title'),'desc','status','content','tag')

    # reverse方法获取后台地址
    def operator(self,obj):
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse('cus_admin:blog_post_change',args=(obj.id,)))

    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)

# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr','object_id','action_flag','user','change_message']






