from django.conf.urls import url
from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date"),
    url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^add_type/$', views.add_type, name='add_type'),
]
