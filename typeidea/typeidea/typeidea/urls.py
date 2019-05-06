"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .custom_site import custom_site
from blog.views import IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView
from config.views import LinkListView
from comment.views import CommentView



urlpatterns = [
    # url(正则字符串，view function，固定参数context，ulr的名称)
    # path('super_admin/', admin.site.urls),
    url(r'super_admin/', admin.site.urls,name="super-admin"),
    # path('admin/', custom_site.urls),
    path(r'admin/', custom_site.urls,name="admin"),
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name="category-list"),
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name="tag-list"),
    url(r'^post/(?P<post_id>\d+).html$',PostDetailView.as_view(),name="post-detail"),
    # url(r'^post/(?P<pk>\d+).html$',PostDetailView.asview(),name="post-detail"),
    # url(r'^links/$',links,name="links"),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^author/(?P<owner_id>\d+)/$',AuthorView.as_view(),name="author"),
    url(r'^links/$',LinkListView.as_view(),name="links"),
    url(r'^comment/$',CommentView.as_view(),name="comment"),

]
