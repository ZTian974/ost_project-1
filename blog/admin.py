from django.contrib import admin
from blog.models import User, Blog, Post, Tag
# Register your models here.

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Tag)
