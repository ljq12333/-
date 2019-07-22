from django.conf.urls import include, url
from django.contrib import admin
from apps.storm.feed import AllArticleRssFeed
urlpatterns = [
    # Examples:
    # url(r'^$', 'ljq_blogs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r"^ljq/", include("user.urls", namespace="ljq")),
    url(r"^category/", include("user.urls", namespace="category")),
    #后台
    url(r"^admin/", include("admin.urls", namespace="admin")),
    #评论
    url(r"^comment/", include("comment.urls", namespace="comment")),
    #使用一些接口规范来使用
    url(r"^api/(?P<version>[v1|v2]+)/", include("user.urls", namespace="api")),
    #RSS订阅
    url(r"^feed/$", AllArticleRssFeed(), name="rss"),
]