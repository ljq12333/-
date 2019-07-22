from storm import models
from django.template import loader


def static_index():
    big_category = models.BigCategory.objects.all()
    #在前台的大分类下面的小分类的实现是通过判断当前的对象通过正向查询判断是不是在小分类的表里面是不是有对应的外键，
    #得到排行数据通过loves的数据来进行升序拿取 在定义表的时候 用过class Meta里面的设置ordering= ["-loves"] 来设置数据库里面数据是通过 降序来得到的
    hot_article = models.CarouselArticle.objects.all()
    order_article = models.Article.objects.all().order_by("-loves")[:5]
    Article_list = models.Article.objects.all()
    status = request.session.get("username")
    big_category = models.BigCategory.objects.all()
    recommend_list = recommendArticle(self, request)