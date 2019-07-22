from django.contrib.syndication.views import Feed
from storm import models


class AllArticleRssFeed(Feed):
    title = "李建强的博客"
    link = "/ljq/index.html"
    description = "最新的一些博客分享"

    def items(self):
        return models.Article.objects.all()[:100]

    def item_title(self, item):
        return "【{}】{}".format(item.category, item.title)

    #显示的内容进行描述
    def item_description(self, item):
        return item.body