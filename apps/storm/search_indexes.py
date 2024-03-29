from haystack import indexes
from storm.models import Article


#指定对于某一个类的数据建立索引
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        print(self.get_model().objects.all())
        return self.get_model().objects.all()