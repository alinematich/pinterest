from django.contrib.auth.models import User as OriginUser
from django.db import models

# Create your models here.

class User(OriginUser):

    def default_weblog(self):
        return self.blog_set.get(default=True)