from django.core import validators
from django.db import models

# Create your models here.
from users.models import User


class Blog(models.Model):
    name = models.CharField(max_length=25, default='Set Name',validators=[validators.validate_slug])
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            temp = self.admin.blog_set.get(default=True)
            if self.default:
                if self != temp:
                    temp.default = False
                    temp.save()
        except Blog.DoesNotExist:
            self.default=True
        super(Blog, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name# + ', admin: ' + self.admin.first_name + ' ' + self.admin.last_name


class Post(models.Model):
    title = models.CharField(max_length=50, validators=[validators.validate_slug])
    summery = models.CharField(max_length=400, validators=[validators.validate_slug])
    text = models.TextField(validators=[validators.validate_slug])
    date = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def author(self):
        return self.blog.admin

    def __str__(self):
        return self.title# + ', blog: ' + str(self.blog)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,validators=[validators.validate_slug])
    text = models.TextField(validators=[validators.validate_slug])
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text + ', post: ' + str(self.post)