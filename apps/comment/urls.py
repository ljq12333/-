from django.conf.urls import url
from comment import views
urlpatterns = [
    url(r"add-comment$", views.CommontView.as_view(), name="add"),
    #拿到自己发表的文章所有的评论
    url(r"blog_user_comms$", views.user_comment.as_view(), name="comment"),
]
