from django.contrib import admin
from blog.models import Blog, Post, Tag
# Register your models here.

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Tag)
