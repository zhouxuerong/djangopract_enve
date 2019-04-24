from django.contrib import admin
from .models import Post,Category,Tag
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_nav','created_time','owner')
    #fields控制页面上的展示
    fields = ('name','status','is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    #查询时url的参数
    parameter_name = "owner_category"

    #返回要展示的内容和查询用的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id","name")

    #根据URL QUERY的内容返回列表页数据
    def queryset(self,request,queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',"category","status","created_time",'owner','operator')
    list_display_links = []
    # 指定哪些字段不展示
    exclude = ('owner',)

    list_filter = [CategoryOwnerFilter,]
    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True
    #fieldsets控制页面的布局
    fieldsets = (
        ('基础配置',{
            'description':"基础配置描述",
            "fields":(
                ("title","category"),
                "status",
            ),
        }),
        ("内容",{
            "fields":(
                "desc",
                "content",
            ),
        }),
        (
            "额外信息",{
                "classes":('collapse',),
                "fields":('tag',),
            })
    )
    # classes 给配置板块加上css属性

    # fields = (('category','title'),'desc','status','content','tag')

    def operator(self,obj):
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse('admin:blog_post_change',args=(obj.id,)))

    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(self,PostAdmin).save_model(request,obj,form,change)

    def post_count(self,obj):
        return obj.post_set.count()

    def get_queryset(self, request):
        qs = super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)

    post_count.short_description="文章数量"

