from django.conf.urls import include, url
from apps.user import views
urlpatterns = [
    #首页
    url(r"index.html/$", views.IndexView.as_view(), name="index"),
    url(r"hjw/(?P<article_id>\d+)$",
        views.ArticleView.as_view(),
        name="article"),
    #生活笔记
    url(r"livenote/$", views.LiveNoteView.as_view(), name="life"),
    url(r"register/$", views.RegisterView.as_view(), name="register"),
    #用户激活
    url(r"active/(?P<token>.+)$", views.user_active.as_view(), name="active"),
    #用户登录
    url(r"login$", views.loginView.as_view(), name="login"),
    #极验验证码
    url(r"check_code/$", views.jyView.as_view(), name="jy"),
    #用户退出
    url(r"user_out$", views.user_out_View.as_view(), name="out"),
    #关于自己
    url(r"self$", views.selfView.as_view(), name="self"),
    #用来爬取博客的文章
    url(r"pq$", views.insertBlog, name="pq"),
    #通过API接口来
    url(r"article/$", views.ArticleApi.as_view(), name="article"),
    #通过关键词的检索来查找将关键字分词  进行再文章中的查找
    url(r"search/$", views.MySearchView(), name="search"),
    #点赞接口的数据验证
    url(r"is_love/$", views.LoveView.as_view(), name="love"),
    #小分类
    url(r"category/(?P<category_id>\d+)$",
        views.CategoryView.as_view(),
        name="category"),
    #技术杂谈
    url(r"technique/$", views.jsView.as_view(), name="js"),
    url(r"shuai/$", views.hjwView.as_view(), name="shuai"),
    #交流
    url(r"exchange$", views.exchangeView.as_view(), name="change"),
    url(r"donate$", views.donate, name="donate")
]