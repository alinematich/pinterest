from functools import wraps
import json
from builtins import print
from django.contrib.auth import authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.utils.decorators import available_attrs

__author__ = 'ali-user'



def test_method(method):
    def _decorator(view_func):
        @wraps(view_func)
        def x(request, *args, **kwargs):
            if request.method == method:
                return view_func(request, *args, **kwargs)
            elif request.method == 'OPTIONS':
                return HttpResponse()
            return err('Send ' + method + ' request, not ' + request.method + ' request')

        return x

    return _decorator


def err(msg):
    return HttpResponse(json.dumps({'status': -1, 'message': msg}), content_type='application/json')


def check_incomplete_data(post=None, get=None):
    if not get:
        get = []
    if not post:
        post = []
    def decorator(func):
        @wraps(func)
        def x(request, *args, **kwargs):
            if request.method == 'POST':
                print(request.POST)
                for i in post:
                    if not i in request.POST:
                        return err('Where is ' + i)
            if request.method == 'GET':
                for i in get:
                    if not i in request.GET:
                        return err('Where is ' + i)
            return func(request, *args, **kwargs)

        return x

    return decorator


def logged_in_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(*args, **kwargs):
        request = None
        if isinstance(args[0], WSGIRequest):
            request = args[0]
            args = args[1:]
        elif len(args[0]) == 3:
            request = args[0][0]
            kwargs = args[0][2]
            args = args[0][1]
        elif len(args) == 2:
            request = args[0][0]
            kwargs = args[1]
            args = args[0][1:]
        if 'HTTP_X_TOKEN' in request.META:
            user = authenticate(token=request.META['HTTP_X_TOKEN'])
            if user:
                request.user = user
                return view_func(request, *args, **kwargs)
            else:
                return err('wrong token')
        else:
            return err('missing token')

    return wrapped_view