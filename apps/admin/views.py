from django.shortcuts import render, redirect, HttpResponse
from storm import models
from comment import models as c_models
# Create your views here.
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import request
from django.utils.decorators import method_decorator
from django.http import QueryDict
import os
from django.conf import settings


#创建判断是否登录的装饰器
def is_session(fun):
    def is_session1(request, *args, **kwargs):
        if request.session.get('username') is None:
            return redirect(reverse('ljq:index'))
        else:
            return fun(request, *args, **kwargs)

    return is_session1


#创建后台主页的CBV
class IndexView(View):
    def get(self, request, *args, **kwargs):
        try:
            return render(request, "admin/index.html")
        except Exception as e:
            print(e)
            return render(request, "admin/index.html")


#添加新的博客CBV
class AddArticleView(View):
    @method_decorator(is_session)
    def get(self, request, *args, **kwargs):
        try:
            article = models.Article.objects.all().first()
            status = request.session.get("username")
            category_list = models.Category.objects.all()
            author = models.Blog_User.objects.filter(name=status).first()
            information = c_models.News.objects.filter(hf_author_id=author.id)
            print(len(information))
            user_toke = models.LoginTake.objects.filter(
                author_id=author.id)[:5]
            information = c_models.News.objects.filter(hf_author_id=author.id)
            if status is None:
                return redirect(reverse("ljq:login"))
            else:
                return render(
                    request, "admin/add-article.html", {
                        "status": status,
                        "category_list": category_list,
                        "author": author,
                        "user_toke": user_toke,
                        "active": "article",
                        "information": information,
                    })
        except Exception as e:
            return render(request, "admin/add-article.html")

    @method_decorator(is_session)
    def post(self, request, *args, **kwargs):
        try:
            body = request.POST.get("content")
            title = request.POST.get("title")
            category = int(request.POST.get("category"))
            status = request.session.get("username")
            author = models.Blog_User.objects.filter(name=status).first()
            summary = "胡继伟为什么变的这么帅"
            img_obj = request.FILES.get("title_img")
            from fdfs_client.client import Fdfs_client
            client_file = os.path.join(settings.BASE_DIR,
                                       "fast_dfs//client.conf")
            res = Fdfs_client(client_file)
            he = res.upload_by_buffer(img_obj.read())
            print(he)
            img_src = settings.BASE_DIR + "\static\images\\" + img_obj.name
            img_link = "/static/images/" + img_obj.name
            with open(img_src, 'wb') as fp:
                for item in img_obj.chunks():
                    fp.write(item)
            article = models.Article.objects.create(title=title,
                                                    author_id=author.id,
                                                    summary=summary,
                                                    category_id=category,
                                                    body=body,
                                                    img_link=img_link)
            slug = "http:127.0.0.1/ljq/hjw/%s" % (str(article.id))
            models.Article.objects.filter(id=article.id).update(slug=slug)
            return redirect(reverse("admin:add_article"))
        except Exception as e:
            print(e)
            return HttpResponse(e)


#管理文章模块
class noticeView(View):
    @method_decorator(is_session)
    def get(self, request, *args, **kwargs):
        try:
            status = request.session.get("username")
            author = models.Blog_User.objects.filter(name=status).first()
            articel_list = models.Article.objects.filter(author_id=author.id)
            user_toke = models.LoginTake.objects.filter(
                author_id=author.id)[:5]
            return render(
                request, "admin/notice.html", {
                    "status": status,
                    "article_list": articel_list,
                    "author": author,
                    "user_toke": user_toke,
                    "active": "article_"
                })
        except Exception as e:
            return render(request, "admin/notice.html")

    @method_decorator(is_session)
    def delete(self, request, *args, **kwargs):
        try:
            delete_list = QueryDict(request.body)
            article_id = delete_list.get("id")
            models.Article.objects.filter(id=article_id).delete()
            return HttpResponse("成功")
        except Exception as e:
            return HttpResponse(e)


#修改密码
class updatePwdView(View):
    @method_decorator(is_session)
    def put(self, request, *args, **kwargs):
        try:
            info = QueryDict(request.body)
            status = request.session.get("username")
            blog = models.Blog_User.objects.filter(
                name=status,
                pwd=info.get("old_password")).update(name=info.get("truename"),
                                                     pwd=info.get("password"))
            if blog is not None:
                del request.session["username"]
                return HttpResponse("成功")
            else:
                return HttpResponse("失败")
        except Exception as e:
            return HttpResponse(e)


#markdownCBV
import markdown
'''
通过文件读取的方式读取上传的.md的文件
使用markdown中自带的函数将.md的格式转换为html标签格式储存到数据库中
 markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
'''


class MarkdownView(View):
    @method_decorator(is_session)
    def get(self, request, *args, **kwargs):
        try:
            article = models.Article.objects.all().first()
            status = request.session.get("username")
            category_list = models.Category.objects.all()
            author = models.Blog_User.objects.filter(name=status).first()
            user_toke = models.LoginTake.objects.filter(
                author_id=author.id)[:5]
            if status is None:
                return redirect(reverse("ljq:login"))
            else:
                return render(
                    request, "admin/add-markdown.html", {
                        "status": status,
                        "category_list": category_list,
                        "author": author,
                        "user_toke": user_toke,
                        "active": "markdown"
                    })
        except Exception as e:
            print(e)
            return render(request, "admin/add-markdown.html")

    @method_decorator(is_session)
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            print(data)
            file_obj = request.FILES.get("md_file")
            mark_body = file_obj.file.read().decode("utf-8")
            models.He.objects.create(body=mark_body)
            html_body = markdown.markdown(
                mark_body,
                extensions=[
                    # 包含 缩写、表格等常用扩展
                    'markdown.extensions.extra',
                    # 语法高亮扩展
                    'markdown.extensions.codehilite',
                ])
            title = request.POST.get("title")
            category = int(request.POST.get("category"))
            author = models.Blog_User.objects.filter(
                name=request.session.get("username")).first().id
            summary = request.POST.get("describe")
            img_obj = request.FILES.get("title_img")
            img_src = settings.BASE_DIR + "\static\images\\" + img_obj.name
            with open(img_src, "wb") as fp:
                for img_bytes in img_obj.chunks():
                    fp.write(img_bytes)
            img_link = "/static/images/" + img_obj.name
            #在这里使用直接读取全部的内容判断所有的条件都符合之后去添加到redis队列当中去  去使用celery来异步的执行存放到数据库的操作
            #这边可以判断当前文件的大小，如果文件的大小大于多少的话，进行异步的写入到数据库当中，如果文件过于小直接在这写入到数据库当中
            #写入到数据库当中
            article = models.Article.objects.create(title=title,
                                                    author_id=author,
                                                    summary=summary,
                                                    category_id=category,
                                                    body=html_body,
                                                    img_link=img_link)
            slug = "http:127.0.0.1/ljq/hjw/%s" % (str(article.id))
            models.Article.objects.filter(id=article.id).update(slug=slug)
            return HttpResponse("成功")
        except Exception as e:
            print(e)
            return HttpResponse(e)


# from django.core.files.uploadedfile import InMemoryUploadedFile
#消息回复管理
class InformationView(View):
    def get(self, request, *args, **kwargs):
        try:
            status = request.session.get("username")
            author = models.Blog_User.objects.filter(name=status).first()
            information_list = c_models.News.objects.filter(
                hf_author_id=author.id)
            user_toke = models.LoginTake.objects.filter(
                author_id=author.id)[:5]
            return render(
                request, "admin/information.html", {
                    "status": status,
                    "active": "information",
                    "information_list": information_list,
                    "user_toke": user_toke
                })
        except Exception as e:
            print(e)
            return HttpResponse(e)

    def post(self, request, *args, **kwargs):
        try:
            print(request.POST)
            hf_content = request.POST.get("content")
            #在这里拿到了三个值 article_id hf_content bhf_author_id 根节点 通过当前的session  拿到回复的人
            c_models.News.objects.filter(
                id=int(request.POST.get("new_id"))).update(
                    hf_content=request.POST.get("content"), is_back=1)
            new_obj = c_models.News.objects.filter(
                id=int(request.POST.get("new_id"))).first()
            status = request.session.get("username")
            user = models.Blog_User.objects.filter(name=status).first()
            c_models.News.objects.create(
                content=hf_content,
                author_id=user.id,
                hf_author_id=int(request.POST.get("bhf_author_id")),
                base_id=int(request.POST.get("base_id")))
            c_models.childrenComment.objects.create(
                content=hf_content,
                parent_id=int(request.POST.get("base_id")),
                article_id=request.POST.get("article_id"),
                author_id=int(request.POST.get("bhf_author_id")),
                bhf_name=new_obj.author.name)
            return HttpResponse("成功")
        except Exception as e:
            print(e)
            return HttpResponse(e)


def change_see(request):
    try:
        new_id = int(request.POST.get("new_id"))
        c_models.News.objects.filter(id=new_id).update(is_see=1)
        return HttpResponse("true")
    except Exception as e:
        return HttpResponse("false")


#更改文章管理
class updateView(View):
    @method_decorator(is_session)
    def get(self, request, *args, **kwargs):
        try:
            article_id = kwargs.get("article_id")
            print(article_id)
            status = request.session.get("username")
            user = models.Blog_User.objects.filter(name=status).first()
            article = models.Article.objects.filter(id=int(article_id),
                                                    author_id=user.id).first()
            user_toke = models.LoginTake.objects.filter(author_id=user.id)[:5]
            information = c_models.News.objects.filter(hf_author_id=user.id)
            if article is None:
                return render(request, "404.html")
            else:
                # assert a = article.body, Exception("报错了")
                # print(a)
                print(article.body)
                return render(
                    request, "admin/update-article.html", {
                        "article": article,
                        "status": status,
                        "user_toke": user_toke,
                        "information": information,
                    })
        except Exception as e:
            print(e)
            return render(request, "404.html")

    @method_decorator(is_session)
    def post(self, request, *args, **kwargs):
        try:
            article_id = kwargs.get("article_id")
            status = request.session.get("username")
            user_obj = models.Blog_User.objects.filter(name=status).first()
            article_obj = models.Article.objects.filter(
                id=int(article_id), author_id=user_obj.id).first()
            if article_obj is None:
                return render(request, "404.html")
            else:
                status = request.session.get("username")
                new_content = request.POST.get("content")
                print(request.POST)
                describe = request.POST.get("describe")
                title = request.POST.get("title")
                models.Article.objects.filter(id=int(article_id),
                                              author_id=user_obj.id).update(
                                                  body=new_content,
                                                  summary=describe,
                                                  title=title)
                return redirect(reverse("admin:notice"))
        except Exception as e:
            print(e)
            return HttpResponse(e)