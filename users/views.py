import json
from builtins import print
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from projeh.decorators import check_incomplete_data, err, logged_in_required, test_method
from users.forms import UserForm
from users.models import User
# Create your views here.
from weblog.models import Blog


@test_method('POST')
@check_incomplete_data(post=['student_number', 'email', 'password', 'first_name', 'last_name'])
def register(request):
    form=UserForm(request.POST)
    if form.is_valid():
        user = User.objects.create_user(form.cleaned_data.get('student_number'), form.cleaned_data.get('email'),
                                        form.cleaned_data.get('password'), first_name=form.cleaned_data.get('first_name'),
                                        last_name=form.cleaned_data.get('last_name'))
        Blog.objects.create(admin=user, default=True)
        return HttpResponse(json.dumps({'status': 0, 'token': default_token_generator.make_token(user)}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': -1, 'error(s)':form.errors}),
                            content_type='application/json')


@test_method('POST')
@check_incomplete_data(post=['student_number', 'password'])
def login(request):
    user = User.objects.get_by_natural_key(request.POST.get('student_number'))
    if user and user.check_password(request.POST.get('password')):
        return HttpResponse(json.dumps({'status': 0, 'token': default_token_generator.make_token(user)}),
                            content_type='application/json')
    else:
        return err('wrong password')


@logged_in_required
def blog_id(request):
    return HttpResponse(json.dumps({'status': 0, 'default-blog': request.user.default_weblog().id}))