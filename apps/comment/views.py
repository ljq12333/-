from django.shortcuts import render, HttpResponse
from django.views.generic import View
from storm import models
from comment import models as c_models


# Create your views here.
#评论的CBV
class CommontView(View):
    def post(self, request, *args, **kwargs):
        try:
            status = request.session.get("username")
            if status is None:
                return HttpResponse("登录之后才能评论")
            else:
                data = request.POST
                #获取评论的内容
                print(request.POST)
                comment_post_ID = data.get("comment_post_ID")
                #评论者
                author = models.Blog_User.objects.filter(name=status).first()
                article_author = models.Article.objects.filter(
                    id=int(comment_post_ID)).first()
                new_content = request.POST.get("w")
                g_id = request.POST.get("g_id")
                print(g_id)
                if g_id == "":
                    comment = c_models.Comment.objects.create(
                        content=new_content,
                        article_id=int(comment_post_ID),
                        author_id=author.id)
                    c_models.News.objects.create(
                        content=new_content,
                        hf_author_id=article_author.author_id,
                        author_id=author.id,
                        base_id=comment.id)
                    li = """<li class="comment byuser comment-author-ljq even thread-even depth-1" id="comment-270938">
                                <div class="c-avatar">
                                    <img alt=''
                                        data-original='/static/images/0.jpg'
                                        class='avatar avatar-54 photo' height='54' width='54' src="/static/images/0.jpg" />
                                    <div class="c-main" id="div-comment-270938">{0}
                                        <div class="c-meta">
                                            <span class="c-author">{1}</span>{2}
                                            <a rel='nofollow' class='comment-reply-link' href="javascript:;"
                                                aria-label='回复给{1}' user_id={3}>回复</a>
                                        </div>
                                    </div>
                                </div>
                            </li>""".format(new_content, author.name,
                                            str(comment.comment_date),
                                            str(author.id))
                    return HttpResponse(li)
                else:
                    bhf_author = models.Blog_User.objects.filter(
                        id=int(request.POST.get("bhf"))).first()
                    c_models.childrenComment.objects.create(
                        content=new_content,
                        parent_id=int(g_id),
                        author_id=author.id,
                        bhf_name=bhf_author.name,
                        article_id=int(comment_post_ID))
                    he = c_models.News.objects.create(
                        content=new_content,
                        hf_author_id=bhf_author.id,
                        author_id=author.id,
                        base_id=int(g_id))
                    li = """
                        <li class="comment byuser comment-author-ljq even thread-even depth-1" id="comment-270938" style="width:80%;margin-left:50px">
                            <div class="c-avatar">
                                <img alt=''
                                    data-original='/static/images/0.jpg'
                                    class='avatar avatar-54 photo' height='54' width='54' />
                                <div class="c-main" id="div-comment-270938">{0}
                                    <div class="c-meta">
                                        <span class="c-author" style="color:red">{1}->{2}</span>{{ {3}|date:'Y-m-d H:i:s' }}
                                        <a rel='nofollow' class='comment-reply-link'
                                            href='javascript:;'
                                            aria-label='回复给{1}' user_id= "{4}">回复</a>
                                    </div>
                                </div>
                            </div>
                        </li>""".format(new_content, author.name,
                                        bhf_author.name, he.create_date,
                                        str(author.id))
                    return HttpResponse(li)
        except Exception as e:
            print(e)
            return HttpResponse(e)


#拿到当前登录用户的对应文章的所有评论
class user_comment(View):
    def get(self, request):
        status = request.session.get("username")
        blog_user = models.Blog_User.objects.filter(name=status).first()
        #首先获取到 当前用户发表的所有的文章的id 列表
        blog_user_article = models.Article.objects.filter(
            author_id=blog_user.id)
        blog_user_article_ids = []
        for article in blog_user_article:
            blog_user_article_ids.append(article.id)
        #获取当前用户发表所有文章的评论
        comment_list = c_models.Comment.objects.filter(
            article_id__in=blog_user_article_ids)
        print(comment_list)
        return render(request, "admin/comment.html", {
            "comment_list": comment_list,
            "status": status,
            "active": "comment"
        })
