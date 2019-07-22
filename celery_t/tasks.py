from celery import Celery, platforms
from django.core.mail import send_mail
import os
import django
from ljq_blogs import settings
from django.template import loader
from django.conf import settings
#加载配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ljq_blogs.settings")
django.setup()
platforms.C_FORCE_ROOT = True
#创建一个celery实例
app = Celery('celery_t.tasks', broker='redis://127.0.0.1:6379/10')


#定义异步的发送邮件
@app.task
def send_register_email(username, email, token):
    #组织邮件信息
    subject = "李建强的个人博客"
    message = ""
    html_message = '<h1>%s,欢迎您注册李建强个人博客网站的成员</h1>点击下面的链接激活您的账号<a href="http://127.0.0.1:8000/ljq/active/%s">点击激活<a/>' % (
        username, token)
    sender = settings.EMAIL_FROM
    receiver = [
        email,
    ]
    print("sb")
    send_mail(subject,
              message,
              sender,
              receiver,
              html_message=html_message,
              fail_silently=False)


#生成静态页面
from storm import models
from django.template import loader


@app.task
def static_index_html():
    big_category = models.BigCategory.objects.all()
    #在前台的大分类下面的小分类的实现是通过判断当前的对象通过正向查询判断是不是在小分类的表里面是不是有对应的外键，
    #得到排行数据通过loves的数据来进行升序拿取 在定义表的时候 用过class Meta里面的设置ordering= ["-loves"] 来设置数据库里面数据是通过 降序来得到的
    hot_article = models.CarouselArticle.objects.all()
    order_article = models.Article.objects.all().order_by("-loves")[:5]
    Article_list = models.Article.objects.all()
    # status = request.session.get("username")
    big_category = models.BigCategory.objects.all()
    recommend_list = models.Article.objects.all().order_by("-views")[:8]
    context = {
        "big_category": big_category,
        "name": "首页",
        "order_article": order_article,
        "article_list": Article_list[:5],
        "recommend_list": recommend_list,
        "hot_articles": hot_article
    }
    #定义模板对象
    temp = loader.get_template("static_index_temp.html")
    #渲染模板
    index_html = temp.render(context)
    #将生成的静态首页的文件对象写入到事先生成的页面中 或者直接创建
    file_path = os.path.join(settings.BASE_DIR, "templates\\static_index.html")
    with open(file_path, 'w', encoding="utf-8") as fp:
        fp.write(index_html)