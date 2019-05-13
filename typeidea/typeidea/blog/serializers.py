from rest_framework import serializers,pagination

from .models import Post,Category

# 文章列表接口
class PostSerializer(serializers.HyperlinkedModelSerializer):
    # SlugRelatedField：外键数据，需要通过SlugRelatedField来配置
    category = serializers.SlugRelatedField(
        read_only=True,   # 定义外键是否可写
        slug_field="name",  # 指定展示的字段
    )
    # 多对多需要配置many
    tag = serializers.SlugRelatedField(
        many = True,
        read_only= True,
        slug_field="name",
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # 数据接口的地址
    url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

    class Meta:
        model = Post
        fields = ['url','id','title','category','tag','owner','created_time']

# 列表详情
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','content_html','created_time' ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_time',]

# 获取分类文章详情
class CategoryDetailSerializer(CategorySerializer):
    # 把posts数据映射到paginated_posts方法上
    posts = serializers.SerializerMethodField("paginated_posts")

    def paginated_posts(self,obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts,self.context['request'])
        serializer = PostSerializer(page,many=True,context={"request":self.context["request"]})
        return {
            "count":posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id','name','created_time','posts'
        )