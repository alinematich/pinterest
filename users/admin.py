from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import ModelAdmin
from users.models import User
from weblog.models import Blog


class BlogAdminInline(admin.TabularInline):
    model = Blog

class UserAdmin(ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = []
    fieldsets = [
        ('user', {'fields': ['username', 'password']}),
        ('info', {'fields': ['first_name', 'last_name', 'email']}),
    ]
    inlines = (BlogAdminInline,)

admin.site.register(User, UserAdmin)