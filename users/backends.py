from builtins import print
from users.models import User

__author__ = 'ali-user'
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator


class TokenBackend(ModelBackend):
    def authenticate(self, username=None, password=None, token=None, **kwargs):
        for user in User.objects.all():
            if default_token_generator.check_token(user,token):
                return user
        return None