from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from storm import models
from itsdangerous import TimedJSONWebSignatureSerializer as jm
from rest_framework.views import APIView
from rest_framework.versioning import URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from django_redis import get_redis_connection
from haystack.views import SearchView
from celery_t.tasks import send_register_email, static_index_html
import time
# Create your views here.
#通过json序列化的类
class ArticleSerializers(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    category_nav_url = serializers.SlugField(source="category.nav_url")
    title = serializers.CharField()
    img_link = serializers.CharField()
    create_date = serializers.DateTimeField()
    views = serializers.IntegerField()
    loves = serializers.IntegerField()
    slug = serializers.SlugField()
    author_name = serializers.CharField(source="author.name")
    id = serializers.IntegerField()
    summary = serializers.CharField()
    class Meta:
        model = models.Article
        fields = [
            'category_name', 'title', 'img_link', 'create_date', 'views',
            'loves', 'slug', 'author_name', 'id', 'category_nav_url','summary'
        ]
#在创建自定义的接口
class ArticleApi(GenericAPIView):
    versioning_class = URLPathVersioning
    #支持解析的数据格式
    parser_classes = [JSONParser, FormParser]
    #form组件的验证校验数据
    serializer_class = ArticleSerializers
    #先得到需要序列化对象的queryset对象
    queryset = models.Article.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            start_index = int(request.data.get("page")) * 5
            end_index = start_index + 5
            res = self.get_queryset()
            article_list = self.get_serializer(instance=res, many=True)
            print(article_list.data[start_index:end_index])
            return Response(article_list.data[start_index:end_index])
        except Exception as e:
            return HttpResponse(e)
#创建主页的CBV
class IndexView(View):
    def get(self, request, *args, **kwargs):
        #得到大分类的QuerySet集合
        try:
            import os
            status = request.session.get("username")
            from django.conf import settings
            file_name = os.path.join(settings.BASE_DIR, "templates\\static_index.html")
            print(file_name)
            if status is None:
                if os.path.isfile(file_name):
                    return render(request, "static_index.html")
                else:
                    static_index_html.delay()
                    time.sleep(2)
                    return render(request, "static_index.html")
            big_category = models.BigCategory.objects.all()
            #在前台的大分类下面的小分类的实现是通过判断当前的对象通过正向查询判断是不是在小分类的表里面是不是有对应的外键，
            #得到排行数据通过loves的数据来进行升序拿取 在定义表的时候 用过class Meta里面的设置ordering= ["-loves"] 来设置数据库里面数据是通过 降序来得到的
            hot_article = models.CarouselArticle.objects.all()
            order_article = models.Article.objects.all().order_by("-loves")[:5]
            Article_list = models.Article.objects.all()
            recommend_list = recommendArticle(self, request)
            return render(
                request, "index1.html", {
                    "big_category": big_category,
                    "name": "首页",
                    "order_article": order_article,
                    "status": status,
                    "article_list": Article_list[:5],
                    "recommend_list": recommend_list,
                    "hot_articles": hot_article
                })
        except Exception as e:
            print(e)
            return HttpResponse(e)


class MessageView(View):
    def get(self, request, *args, **kwargs):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(e)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(e)


class LiveNoteView(View):
    def get(self, request, *args, **kwargs):
        try:
            is_big_category = models.BigCategory.objects.filter(
                name="生活笔记").first()
            if is_big_category is not None:
                big_category = models.BigCategory.objects.all()
                category = models.Category.objects.filter(bigcategory_id=is_big_category.id)
                hot_article = models.CarouselArticle.objects.all()
                status = self.request.session.get("username")
                recommend_list = recommendArticle(self, self.request)
                return render(
                    request, "life.html", {
                        "big_category": big_category,
                        "hot_article": hot_article,
                        "status": status,
                        "recommend_list": recommend_list,
                        "categorys": category,
                        "name": "生活笔记"
                    })
            else:
                return render(request, "404.html")
        except Exception as e:
            print(e)
            return HttpResponse(e)

#技术杂谈
class jsView(View):
    def get(self, request, *args, **kwargs):
        try:
            is_big_category = models.BigCategory.objects.filter(
                    name="技术杂谈").first()
            if is_big_category is not None:
                big_category = models.BigCategory.objects.all()
                category = models.Category.objects.filter(
                    bigcategory_id=is_big_category.id)
                return render(
                    request, "life.html", {
                        "big_category": big_category,
                        "categorys": category,
                        "name": "技术杂谈"
                    })
            else:
                return render(request, "404.html")
        except Exception as e:
            print(e)
            return HttpResponse(e)
#胡继伟最帅
class hjwView(View):
    def get(self, request, *args, **kwargs):
        try:
            is_big_category = models.BigCategory.objects.filter(
                    name="胡继伟最帅").first()
            if is_big_category is not None:
                big_category = models.BigCategory.objects.all()
                category = models.Category.objects.filter(
                    bigcategory_id=is_big_category.id)
                return render(
                    request, "life.html", {
                        "big_category": big_category,
                        "categorys": category,
                        "name": "胡继伟最帅"
                    })
            else:
                return render(request, "404.html")
        except Exception as e:
            print(e)
            return HttpResponse(e)
class exchangeView(View):
     def get(self, request, *args, **kwargs):
        try:
            is_big_category = models.BigCategory.objects.filter(
                    name="技术交流").first()
            if is_big_category is not None:
                big_category = models.BigCategory.objects.all()
                category = models.Category.objects.filter(
                    bigcategory_id=is_big_category.id)
                return render(
                    request, "exchange.html", {
                        "big_category": big_category,
                        "categorys": category,
                        "name": "技术交流"
                    })
            else:
                return render(request, "404.html")
        except Exception as e:
            print(e)
            return HttpResponse(e)
#用来添加博客
def insertBlog(request):
    try:
        import requests
        from lxml import etree
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        url = "https://stormsha.com/"
        response = requests.get(url, headers=headers)
        res = response.text
        html = etree.HTML(res)
        article_list = html.xpath(
            "//div[@class='content']/article/header/h2/a/@href")
        for item in article_list:
            response = requests.get(item, headers=headers)
            res = response.text
            html = etree.HTML(res)
            article = html.xpath("//article")[0]
            t = etree.tostring(article, encoding="utf-8", pretty_print=True)
            title = html.xpath("//h1[@class='article-title']/a/text()")[0]
            body = t.decode("utf-8")
            summary = html.xpath('//h1[@class="article-title"]/a')[0].text
            import random
            models.Article.objects.create(author_id=1,
                                          body=body,
                                          summary=summary,
                                          title=title,
                                          views=1000,
                                          loves=1000,
                                          category_id=random.randint(1, 3),
                                          img_link="https://www.baidu.com",
                                          slug="https://www.beaad.com/" +
                                          str(random.randint(1, 1000)) + "")
        return HttpResponse("成功")
    except Exception as e:
        print(e)
        return HttpResponse(e)


#显示文章的详情页面
class ArticleView(View):
    def get(self, request, *args, **kwargs):
        user_name = request.session.get("username")
        article_id = kwargs.get("article_id")
        if article_id is None:
            return render(request, "404.html")
        else:
            article = models.Article.objects.filter(id=article_id).first()
            if article is None:
                return render(request, "404.html")
            else:
                from comment import models as c_models
                comment_list = c_models.Comment.objects.filter(
                    article_id=article_id)
                prev_article = prevArticle(article_id)
                next_article = nextArticle(article_id)
                article = models.Article.objects.get(id=article_id)
                name = models.Article.objects.filter(
                    id=article_id).first().category.bigcategory.name
                models.Article.objects.filter(id=article_id).update(
                    views=(article.views + 1))
                big_category = models.BigCategory.objects.all()
                redis = get_redis_connection("default")
                if user_name is None:
                    ip = request.META["REMOTE_ADDR"]
                    redis.lpush(ip, article_id)
                else:
                    user_id = models.Blog_User.objects.filter(
                        name=user_name).first().id
                    redis.lpush(user_id, article_id)
                return render(
                    request, "article.html", {
                        "big_category": big_category,
                        "article": article,
                        "prev_article": prev_article,
                        "next_article": next_article,
                        "status": user_name,
                        "comment_list": comment_list,
                        "name": name,
                    })
        return HttpResponse(article_id)


#用来判断并且获取当前文章的上一篇
def prevArticle(article_id):
    prev_status = False
    article_id = int(article_id)
    print(article_id)
    prev_id = article_id - 1
    while prev_id > 0 and not prev_status:
        prev_article = models.Article.objects.filter(id=prev_id).first()
        if prev_article is None:
            prev_id -= 1
        else:
            prev_status = True
    if prev_status:
        print(prev_id)
        article = models.Article.objects.filter(id=prev_id).first()
        return article
    else:
        print(prev_id)
        return None


#用来判断并且获取下一篇文章
def nextArticle(article_id):
    next_status = False
    article_id = int(article_id)
    max_article = models.Article.objects.all().order_by("-id").first()
    max_id = max_article.id
    next_id = article_id + 1
    while next_id <= max_id and not next_status:
        next_article = models.Article.objects.filter(id=next_id).first()
        if next_article is None:
            next_id += 1
        else:
            next_status = True
    if next_status:
        article = models.Article.objects.filter(id=next_id).first()
        return article
    else:
        return None


from django.forms import Form, fields


class RegisterForm(Form):
    name = fields.CharField(max_length=10,
                            required=True,
                            min_length=3,
                            error_messages={
                                "max_length": "用户名的长度最大为20",
                                "min_length": "用户名的长度最小为3",
                                "required": "用户名不能为空"
                            })
    email = fields.EmailField(required=True,
                              error_messages={
                                  'required': u'邮箱不能为空',
                                  'invalid': u'邮箱格式错误'
                              })
    pwd = fields.CharField(required=True,
                           min_length=6,
                           max_length=16,
                           error_messages={
                               "max_length": "密码长度不能超过16位",
                               "min_length": "密码长度必须在6位以上",
                               "required": "密码不能为空"
                           })


#注册视图
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        try:
            big_category = models.BigCategory.objects.all()
            return render(request, "register.html",
                          {"big_category": big_category})
        except Exception as e:
            return render(request, "404.html")

    def post(self, request, *args, **kwargs):
        try:
            import json
            big_category = models.BigCategory.objects.all()
            form_obj = RegisterForm(request.POST)
            form_data = json.dumps(request.POST, ensure_ascii=False)
            if form_obj.is_valid():
                if request.POST.get("pwd") != request.POST.get("pwd1"):
                    form_error = {"pwd1": "两次密码要相同"}
                    blog_user = models.Blog_User.objects.filter(
                        name=request.POST.get("name")).first()
                    if blog_user is None:
                        form_error.get("is_name", "该用户名已经存在")
                    email_count = models.Blog_User.objects.filter(
                        email=request.POST.get("email"))
                    if email_count.count() == 3:
                        form_error.get("max_email", "该邮箱已经达到最大的注册量")
                    return render(
                        request, "register.html", {
                            "big_category": big_category,
                            "form_error": form_error,
                            "form_data": json.loads(form_data)
                        })
                else:
                    user_obj = models.Blog_User.objects.create(
                        **form_obj.cleaned_data)
                    #创建加密对象 秘钥为ljq,有效时间为一个小时
                    jm1 = jm("ljq", 3600)
                    xx = {"confim": user_obj.id}
                    token = jm1.dumps(xx).decode("utf-8")
                    print(request.POST.get("email").strip())
                    send_register_email.delay(
                        request.POST.get("name"),
                        request.POST.get("email").strip(), token)
                    return render(request, "register.html", {
                        "big_category": big_category,
                        "status": 1
                    })
            else:
                return render(
                    request, "register.html", {
                        "form_error": form_obj.errors,
                        "big_category": big_category,
                        "form_data": json.loads(form_data)
                    })
        except Exception as e:
            print(e)
            return HttpResponse(e)


#用户激活视图类
class user_active(View):
    def get(self, request, token):
        try:
            if token is None:
                return HttpResponse("不合法的激活地址")
            else:
                import json
                jm1 = jm('ljq', 3600)
                user_dict = jm1.loads(token)
                user_id = user_dict.get("confim")
                models.Blog_User.objects.filter(id=user_id).update(is_active=1)
                return HttpResponse("激活成功")
        except Exception as e:
            print(e)
            return HttpResponse("激活链接失效")


class loginView(View):
    big_category = models.BigCategory.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            return render(request, "login.html",
                          {"big_category": self.big_category})
        except Exception as e:
            return render(request, "login.html",
                          {"big_category": self.big_category})

    def post(self, request):
        try:
            email = request.POST.get("email")
            pwd = request.POST.get("pwd")
            pc_geetest_id = "d25d66e1eba4a79b97cbe360f4932617"
            pc_geetest_key = "5adc3a6f063632aff82ea78a16db6b03"
            gt = GeetestLib(pc_geetest_id, pc_geetest_key)
            challenge = request.POST.get("geetest_challenge", "")
            validate = request.POST.get("geetest_validate", "")
            seccode = request.POST.get("geetest_seccode", "")
            status = request.session[gt.GT_STATUS_SESSION_KEY]
            user_id = request.session["user_id"]
            result = gt.success_validate(challenge, validate, seccode,
                                                user_id)
            if email != "" and pwd != "":
                if result != 1:
                    return render(request, "login.html", {
                        "login_email": email,
                        "login_status": 1,
                        "big_category": self.big_category
                    })
                user = models.Blog_User.objects.filter(email=email,
                                                       pwd=pwd).first()
                if user is not None:
                    if user.is_active == 1:
                        ip = request.META['REMOTE_ADDR']
                        models.LoginTake.objects.create(ip=ip,
                                                        status=1,
                                                        author_id=user.id)
                        request.session["username"] = user.name
                        return redirect(reverse("ljq:index"))
                    else:
                        return render(request, "login.html", {
                            "login_email": email,
                            "login_status": 4,
                            "big_category": self.big_category
                        })
                else:
                    return render(request, "login.html", {
                        "login_email": email,
                        "login_status": 2,
                        "big_category": self.big_category
                    })
            else:
                return render(request, "login.html", {
                    "login_email": email,
                    "login_status": 3,
                    "big_category": self.big_category
                })
        except Exception as e:
            print(e)
            return HttpResponse(e)


#极验验证码
from geetest import GeetestLib


class jyView(View):
    pc_geetest_id = "d25d66e1eba4a79b97cbe360f4932617"
    pc_geetest_key = "5adc3a6f063632aff82ea78a16db6b03"

    def get(self, request, *args, **kwargs):
        try:
            user_id = "jjjj"
            gt = GeetestLib(self.pc_geetest_id, self.pc_geetest_key)
            status = gt.pre_process(user_id)
            request.session[gt.GT_STATUS_SESSION_KEY] = status
            request.session["user_id"] = user_id
            response_str = gt.get_response_str()
            print(response_str)
            return HttpResponse(response_str)
        except Exception as e:
            print(e)
            return HttpResponse(e)


class user_out_View(View):
    def get(self, request, *args, **kwargs):
        try:
            del request.session["username"]
            return redirect(reverse("ljq:index"))
        except Exception as e:
            print(e)
            return HttpResponse(e)


#关于自己
class selfView(View):
    def get(self, request, *args, **kwargs):
        try:
            big_category = models.BigCategory.objects.all()
            status = request.session.get("username")
            return render(request, "about.html", {
                "big_category": big_category,
                "status": status,
                "name": "自我介绍"
            })
        except Exception as e:
            print(e)
            return HttpResponse(e)


#猜你喜欢
'''
1. 后台通过当前用浏览的文章 存放到redis数据库里面的list类型中  每一个人的id 对应一个list   
2. 如果是没有登录的用户， 选取用户的ip 当做list的键来存放浏览过的数据
3. 如果当前用户是第一次登录没有浏览记录， 后台会通过浏览次数最多的前几个文章推荐给用户
'''


#推荐文章
def recommendArticle(self, request):
    username = request.session.get("username")
    status = models.Blog_User.objects.filter(name=username).first()
    if status is not None:
        #获取当前用户的id
        user_id = status.id
        redis = get_redis_connection("default")
        b_id = bytes(str(user_id), encoding="utf-8")
        if b_id in redis.keys("*"):
            id_list = redis.lrange(user_id, 0, -1)
            #获取到存储在Redis数据库中的文章的ID  通过使用__in 来获取到所对应的Article对象
            recommend_list = models.Article.objects.filter(id__in=id_list)
            return recommend_list
        else:
            recommed_list = models.Article.objects.all().order_by("-views")[:8]
            return recommed_list
    else:
        ip = request.META['REMOTE_ADDR']
        redis = get_redis_connection("default")
        b_ip = bytes(str(ip), encoding="utf-8")
        if b_ip in redis.keys("*"):
            id_list = redis.lrange(ip, 0, -1)
            print(id_list)
            recommend_list = models.Article.objects.filter(id__in=id_list)
            return recommend_list
        #对得到的list里面的数据进行去重
        else:
            recommend_list = models.Article.objects.all().order_by(
                "-views")[:8]
            return recommend_list
from django.http import request
class MySearchView(SearchView):
    template = "search_list.html" #自定义自己的模板渲染的页面地址
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        big_category = models.BigCategory.objects.all()
        hot_article = models.CarouselArticle.objects.all()
        status = self.request.session.get("username")
        recommend_list = recommendArticle(self, self.request)
        context["big_category"] = big_category
        context["status"] = status
        context["hot_article"] = hot_article
        context["recommend_list"] = recommend_list
        return context
#点赞 CBV
class LoveView(View):
    def post(self, request, *args, **kwargs):
        try:
            status = request.session.get("username")
            if status is None:
                return HttpResponse("false")
            else:
                redis = get_redis_connection("default")
                keys = redis.keys("*")
                user_id = models.Blog_User.objects.filter(name=status).first().id
                love_ = "love_%s"%(str(user_id))
                b_id = bytes(str(love_), encoding="utf-8")
                article_id = int(request.POST.get("um_id"))
                if b_id in keys:
                    b_article_id = bytes(str(article_id), encoding="utf-8")
                    print(b_article_id)
                    article_id_list = redis.lrange(love_, 0, -1)
                    print(article_id_list)
                    if b_article_id in article_id_list:
                        return HttpResponse("active")
                    else:
                        redis.lpush(love_, article_id)
                        old_love = models.Article.objects.filter(id=article_id).first()
                        models.Article.objects.filter(id=article_id).update(loves=(old_love.loves+1))
                        return HttpResponse("ok")
                else:
                    love_id = "love_%s"%(str(user_id))
                    redis.lpush(b_id, article_id)
                    return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse(e)
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        try:
            category_id = kwargs.get("category_id")
            if category_id is None:
                return render(request, "404.html")
            else:
                category = models.Category.objects.filter(id=category_id).first()
                if category is not None:
                    big_category = models.BigCategory.objects.all()
                    name = category.bigcategory.name
                    hot_article = models.CarouselArticle.objects.all()
                    status = request.session.get("username")
                    recommend_list = recommendArticle(self, request)
                    article = models.Article.objects.all()
                    return render(request, "category.html",{"big_category": big_category,"name": name, "category": category, "status": status, "hot_articles": hot_article, "recommend_list": recommend_list})
                else:
                    return render(request, "404.html")
        except Exception as e:
            print(e)
            return render(request, "404.html")
#跳转到打赏页面
def donate(request):
    try:
        status = request.session.get("username")
        big_category = models.BigCategory.objects.all()
        return render(request, "donate.html", {"status": status, "big_category":big_category,"name": "打赏作者"})
    except Exception as e:
        print(e)
        return render(request, "donate.html", {"status": status, "big_category":big_category,"name": "打赏作者"})