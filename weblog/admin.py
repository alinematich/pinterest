from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from weblog.models import Blog, Post, Comment


class PostInline(admin.TabularInline):
    model = Post


class BlogAdmin(ModelAdmin):
    list_display = ['name', 'admin', 'default']
    search_fields = ['name', 'admin']
    list_filter = ['admin', 'default']
    fields = ['name', 'admin', 'default']
    inlines = (PostInline,)


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(ModelAdmin):
    list_display = ['title', 'blog', 'author', 'date']
    search_fields = ['title', 'summery', 'text']
    list_filter = ['date', 'blog']
    fieldsets = [('Post', {'fields': ['title', 'summery', 'text']}),
                 ('info', {'fields': ['blog']})
    ]
    inlines = (CommentInline,)


class CommentAdmin(ModelAdmin):
    list_display = ['post', 'text', 'date']
    search_fields = ['text']
    list_filter = ['date', 'post']
    fields = ['post', 'text']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment,CommentAdmin)