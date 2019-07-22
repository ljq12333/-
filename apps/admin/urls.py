from django.conf.urls import url
from apps.admin import views
urlpatterns = [
    #添加文章
    url(r"add-article$", views.AddArticleView.as_view(), name="add_article"),
    #后台主页
    url(r"index$", views.IndexView.as_view(), name="index"),
    #公告
    url(r"notice$", views.noticeView.as_view(), name="notice"),
    #修改信息
    url(r"info_update$", views.updatePwdView.as_view(), name="info_update"),
    #上传markdown文件
    url(r"add_markdown$", views.MarkdownView.as_view(), name="markdown"),
    url(r"information$", views.InformationView.as_view(), name="information"),
    #更改用户的消息查看状态
    url(r"change_see$", views.change_see, name="see_change"),
    #更改文章内容
    url(r"update_article/(?P<article_id>\d+)$",
        views.updateView.as_view(),
        name="update_article")
]
