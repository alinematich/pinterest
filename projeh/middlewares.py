from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponsePermanentRedirect
from projeh import settings
from projeh.decorators import err
from users.models import User
from weblog.models import Blog, Post, Comment

__author__ = 'ali-user'

class Cors_Middleware(object):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'origin, x-token, content-type, accept, user_agent, access_control_request_method, access_control_request_headers, accept_language, host, accept_encoding, referer, connection'
        return response


    def get_full_path_with_slash(self, request):
        if settings.DEBUG:
            raise RuntimeError('pfff')
        return request.get_full_path(force_append_slash=True)

    def process_exception(self,request,exception):
        if isinstance(exception,User.DoesNotExist):
            return err("User not found")
        if isinstance(exception,Blog.DoesNotExist):
            return err("Blog not found")
        if isinstance(exception,Post.DoesNotExist):
            return err("Post not found")
        if isinstance(exception,Comment.DoesNotExist):
            return err("Comment not found")
        if isinstance(exception, RuntimeError) and request.method=='POST':
            return HttpResponsePermanentRedirect(self.get_full_path_with_slash(request))
        return None