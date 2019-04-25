from django.contrib.admin import AdminSite

# 定义自己的站点，修改app下register部分代码
class CustomSite(AdminSite):
    site_header = "Typeider"
    site_title = "博客管理后台"
    index_title = "首页"

custom_site = CustomSite(name="cus_admin")