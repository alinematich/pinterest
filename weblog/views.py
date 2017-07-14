import json
from builtins import print
from django.http import HttpResponse
# Create your views here.
from projeh.decorators import logged_in_required, check_incomplete_data, err, test_method
from weblog.models import Post, Blog


@test_method('GET')
@logged_in_required
def posts(request, blog_id=-1):
    if blog_id == -1:
        blog_id = request.user.default_weblog().id
    blog = Blog.objects.get(pk=blog_id)
    count = blog.post_set.count()
    offset = 0
    if 'offset' in request.GET:
        offset = int(request.GET['offset'])
    if 'count' in request.GET:
        count = int(request.GET['count']) + offset
    if count > blog.post_set.count():
        count = blog.post_set.count
    data = blog.post_set.all().order_by('-date')[offset:count]
    postls = [{"id": d.id, "title": d.title, "summery": d.summery, "datetime": str(d.date)}
              for d in data]
    return HttpResponse(json.dumps({'status': 0, 'posts': postls}), content_type='application/json')


@logged_in_required
@check_incomplete_data(get=['id'], post=['title', 'summary', 'text'])
def post(request, blog_id=-1):
    if request.method == 'GET':
        id = request.GET['id']
        if blog_id == -1:
            post = Post.objects.get(pk=id)
        else:
            blog = Blog.objects.get(pk=blog_id)
            post = blog.post_set.get(pk=id)
        return HttpResponse(json.dumps({'status': 0,
                                        'post': {'title': post.title, 'summery': post.summery, 'text': post.text,
                                                 'datetime': str(post.date)}}), content_type='application/json')
    if request.method == 'POST':
        if blog_id == -1:
            blog = request.user.default_weblog()
        else:
            blog = Blog.objects.get(pk=blog_id)
        if blog.admin != request.user:
            return err('not allowed!')
        post = blog.post_set.create(title=request.POST['title'], summery=request.POST['summary'],
                                    text=request.POST['text'], blog=blog)
        return HttpResponse(json.dumps({'status': 0, 'post_id': post.id}), content_type='application/json')


@test_method('GET')
@logged_in_required
@check_incomplete_data(get=['post_id'])
def comments(request, blog_id=-1):
    post_id = request.GET['post_id']
    if blog_id == -1:
        post = Post.objects.get(pk=post_id)
    else:
        blog = Blog.objects.get(pk=blog_id)
        post = blog.post_set.get(pk=post_id)
    count = post.comment_set.count()
    offset = 0
    if 'offset' in request.GET:
        offset = int(request.GET['offset'])
    if 'count' in request.GET:
        count = int(request.GET['count']) + offset
    if count > post.comment_set.count():
        count = post.comment_set.count()
    data = post.comment_set.all().order_by('-date')[offset:count]
    commentls = [{"text": d.text, "datetime": d.date}
                 for d in data]
    return HttpResponse(json.dumps({'status': 0, 'comments': commentls}))


@test_method('POST')
@logged_in_required
@check_incomplete_data(post=['post_id', 'text'])
def comment(request, blog_id=-1):
    if blog_id == -1:
        post = Post.objects.get(pk=request.POST['post_id'])
    else:
        blog = Blog.objects.get(pk=blog_id)
        post = blog.post_set.get(pk=request.POST['post_id'])
    post.comment_set.create(post=post, text=request.POST['text'])