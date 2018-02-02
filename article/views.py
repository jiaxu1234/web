#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #分页

from django.contrib.syndication.views import Feed

# Create your views here.
def home(request):
    posts = Article.objects.all()  #获取全部的Article对象
    paginator = Paginator(posts, 10) #每页显示两个
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list' : post_list})

# def detail1(request, my_args):
#     post = Article.objects.all()[int(my_args)]
#     str = ("title = %s, category = %s, date_time = %s, content = %s"
#         % (post.title, post.category, post.date_time, post.content))
#     return HttpResponse(str)

def detail2(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post})


def test(request) :
    return render(request, 'test.html', {'current_time': datetime.now()})

def search_tag(request, tag) :
    try:
        post_list = Article.objects.filter(category = tag) #contains
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

def output(request) :
    return render(request, 'output.html', {'current_time': datetime.now()})



##########################################以下为RSS
class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content