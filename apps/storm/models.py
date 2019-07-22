from django.db import models
from user import models as u_models
from ljq_blogs import settings
from django.core.urlresolvers import reverse
# Create your models here.
import markdown
#登录记录
takestatus = ((1, "成功"), (0, "失败"))


#轮播展示的书籍的数据
class CarouselArticle(models.Model):
    img_link = models.SlugField(unique=True)
    name = models.CharField(max_length=40)
    article = models.ForeignKey(to="Article", )

    class Meta:
        db_table = "carouse_article"


class LoginTake(models.Model):
    ip = models.CharField(max_length=30)
    take_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=takestatus)
    author = models.ForeignKey(to="Blog_User", )

    class Meta:
        db_table = "login_take"


class BigCategory(models.Model):
    # 导航名称
    name = models.CharField('文章大分类', max_length=20)
    # 用作文章的访问路径，每篇文章有独一无二的标识，下同
    nav_url = models.SlugField(unique=True)
    # 分类页描述
    description = models.TextField('描述',
                                   max_length=240,
                                   default="李建强",
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    # 分类页Keywords
    keywords = models.TextField('关键字',
                                max_length=240,
                                default="李建强",
                                help_text='用来作为SEO中keywords,长度参考SEO标准')

    class Meta:
        verbose_name = '大分类'
        verbose_name_plural = verbose_name
        db_table = "BigCategory"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60)
    nav_url = models.SlugField(unique=True)
    description = models.TextField('描述',
                                   max_length=240,
                                   default="ljq",
                                   help_text='用来写当前的小分类的博客的描述')
    bigcategory = models.ForeignKey(
        to="BigCategory",
        verbose_name="外键大分类",
    )

    class Meta:
        verbose_name = '小分类'
        verbose_name_plural = verbose_name
        ordering = ['name']
        db_table = "Category"


#标签
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述',
                                   max_length=240,
                                   default="李建强",
                                   help_text='写当前标签的描述')

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        db_table = "Tag"
        ordering = ["id"]


#搜索的关键字
class Keyword(models.Model):
    name = models.CharField('关键字的名字', max_length=20)

    class Meta:
        verbose_name = '关键字'
        verbose_name_plural = verbose_name
        ordering = ['name']
        db_table = "Keyword"

    def __str__(self):
        return self.name


#博客用户
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Blog_User(models.Model):
    name = models.CharField(max_length=20)
    link = models.URLField(verbose_name="博客用户的链接",
                           blank=True,
                           help_text="当前博客用户的链接")
    pwd = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    is_active = models.IntegerField(default=0)

    class Meta:
        verbose_name = "博客用户",
        verbose_name_plural = verbose_name
        db_table = "Blog_User"


#文章
# from taggit.managers import TaggableManager


class Article(models.Model):
    #文章图片的链接 指向文章的显示的地址
    # Tag = TaggableManager(blank=True)
    IMG_LINK = '/static/images/summary.jpg'
    # 写当前文章的作者 充当外键
    author = models.ForeignKey(to="Blog_User", verbose_name='作者')
    title = models.CharField(max_length=150, verbose_name='文章的标题')
    summary = models.TextField('简要的', max_length=230, default='介绍文章的简要说明')
    #文章的主体
    body = models.TextField(verbose_name='文章的主要内容')
    img_link = models.CharField('?????', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建的时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新的时间', auto_now=True)
    views = models.IntegerField(verbose_name='文章观看的次数', default=0)
    loves = models.IntegerField('文章获得到的点赞数', default=0)
    #文章的跳转的地址
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name='文章属于什么种类的')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    keywords = models.ManyToManyField(Keyword,
                                      verbose_name='关键字',
                                      help_text='文章里面的关键字')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']
        db_table = "Article"

    def get_absolute_url(self):
        return reverse("ljq:article", kwargs={"article_id": self.id})


#公告表  用来子啊页面的右边显示 和别的表没有什么关联
class Activate(models.Model):
    text = models.TextField('公告的文本', null=True)
    is_active = models.BooleanField('是否激活', default=False)
    add_date = models.DateTimeField('添加的时间', auto_now_add=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name
        db_table = "Activate"


#友情链接
class FriendLink(models.Model):
    name = models.CharField('友情连接的名字', max_length=50)
    description = models.CharField('描述', max_length=100, blank=True)
    link = models.URLField('链接', help_text='跳转到友情链接的地址')
    logo = models.URLField('友情链接的logo', help_text='友情链接的logo图片', blank=True)
    create_date = models.DateTimeField('创建的时间', auto_now_add=True)
    is_active = models.BooleanField('是否被激活', default=True)
    is_show = models.BooleanField('是否展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']
        db_table = "FriendLink"


class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    is_active = models.IntegerField(default=0)

    class Meta:
        db_table = "user"


class He(models.Model):
    body = models.TextField(verbose_name='文章的主要内容')

    class Meta:
        db_table = 'he'