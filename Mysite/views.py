import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum, Q
from django.core.cache import cache

from Mysite.forms import RegForm, LoginForm
from blog import models
from blog.forms import ArticleForm
from read_statistics.utils import *
from blog.models import Blog, BlogType


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


def get_month_hot_blogs():
    today = timezone.now().date()
    monthday = calendar.monthrange(today.year, today.month)[1]
    date = today - datetime.timedelta(days=monthday)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:monthday]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    week_dates, read_nums_of_week = get_seven_days_read_data(blog_content_type)
    month_dates, read_num_of_month = get_month_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    hot_blogs_for_month = cache.get('hot_blogs_for_month')

    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
    elif hot_blogs_for_7_days != get_7_days_hot_blogs():
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
    if hot_blogs_for_month is None:
        hot_blogs_for_month = get_month_hot_blogs()
        cache.set('hot_blogs_for_month', hot_blogs_for_month, 3600)
    elif hot_blogs_for_month != get_month_hot_blogs():
        hot_blogs_for_month = get_month_hot_blogs()
        cache.set('hot_blogs_for_month', hot_blogs_for_month, 3600)
    context = {}
    context['dates'] = week_dates
    context['read_nums'] = read_nums_of_week
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    context['hot_blogs_for_month'] = hot_blogs_for_month
    return render(request, 'home.html', context)


def add_type(request):
    if request.method == 'POST':
        new_type_name = request.POST.get('name')
        # models.Book.objects.create(name=new_book_name, publisher_id=publisher_id)
        models.BlogType.objects.create(type_name=new_type_name)
        return redirect('post_new')
    res = models.BlogType.objects.all()
    return render(request, 'add_blog_type.html', {"blog_type": res})


def search(request):
    search_words = request.GET.get('wd', '').strip()
    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    search_blogs = []
    if condition is not None:
        # 筛选：搜索
        search_blogs = Blog.objects.filter(condition)

    # 分页
    paginator = Paginator(search_blogs, 20)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)

    context = {}
    context['search_words'] = search_words
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'search.html', context)