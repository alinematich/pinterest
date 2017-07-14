from django.conf.urls import url
from weblog import views

__author__ = 'ali-user'

urlpatterns=[
    url(r'^posts/',views.posts, name='posts'),
    url(r'^(?P<blog_id>[0-9]+)/posts/',views.posts,name='postsid'),
    url(r'^post/',views.post,name='post'),
    url(r'^(?P<blog_id>[0-9]+)/post/',views.post,name='postid'),
    url(r'^comments/',views.comments,name='comments'),
    url(r'^(?P<blog_id>[0-9]+)/comments/',views.comments,name='commentsid'),
    url(r'^comment/',views.comment,name='comment'),
    url(r'^(?P<blog_id>[0-9]+)/comment/',views.comment,name='commentid'),
]