from django.conf.urls import url
import users.views
__author__ = 'ali-user'

urlpatterns = [
    url(r'^register/', users.views.register, name='register'),
    url(r'^login/', users.views.login, name='login'),
    url(r'^blog_id/',users.views.blog_id, name='blog_id'),
]