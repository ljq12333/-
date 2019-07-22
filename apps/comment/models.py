from django.db import models


# Create your models here.
class Comment(models.Model):
    content = models.TextField(max_length=100, default=False)
    article = models.ForeignKey("storm.Article")
    author = models.ForeignKey("storm.Blog_User")
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name
        ordering = ['-comment_date']
        db_table = "comment"


#子回复每一条的评论下面都可能有子回复
class childrenComment(models.Model):
    content = models.TextField(max_length=100, default=False)
    parent = models.ForeignKey("Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("storm.Blog_User")
    bhf_name = models.CharField(max_length=20)
    article = models.ForeignKey("storm.Article")

    class Meta:
        verbose_name = "根评论下面的子评论"
        ordering = ["-comment_date"]
        db_table = "children_comment"


back = ((0, "未回复"), (1, "回复"))
see = ((0, "未看"), (1, "以看"))
#你要是回复消息  必须的已知条件
'''
1. 你给谁回复
2. 你们消息讨论的根节点是谁
3. 回复的是哪一篇文章的
--------回复消息等同于给人又发送了消息该如何将消息发送出去
1. 现在你是回复者 而回复你消息的人成为了被回复者
2. 你们回复消息的根节点
'''


class News(models.Model):
    content = models.CharField(max_length=60)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    hf_content = models.CharField(max_length=60)
    #被回复的作者
    hf_author = models.ForeignKey("storm.Blog_User")
    #是否回复
    is_back = models.IntegerField(choices=back, default=0)
    #是否看过消息
    is_see = models.IntegerField(choices=see, default=0)
    author = models.ForeignKey("storm.Blog_User", related_name="author_1")
    base = models.ForeignKey("Comment")

    class Meta:
        verbose_name = "消息通知"
        ordering = ["-create_date"]
        db_table = "news"