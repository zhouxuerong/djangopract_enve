from rest_framework import serializers

from .models import Post

# 文章列表接口
class PostSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','created_time']

# 列表详情
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','content_html','created_time' ]