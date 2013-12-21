from models import Blog,Post,Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import uuid
import os
from django.core.files import File
from django.conf import settings

import datetime
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class RssFeed(Feed):
    title = "OST Project"
    link = "http://ec2-54-200-28-13.us-west-2.compute.amazonaws.com/blog/"
    description = "Wenjie Chen's Blog"
    feed_type = CorrectMimeTypeFeed

    def get_object(self, request, blog_id=None):
        return Blog.objects.get(pk=blog_id)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return reverse('blog:blog_posts', kwargs={'slug': obj.slug})

    def description(self, obj):
        return obj.title

    def author_name(self, obj):
        return '%s' % (obj.user.username)

    def author_email(self, obj):
        return obj.user.email

    def items(self, obj):
        return obj.post_set.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = item.body
        return content

    def item_link(self, item):
        return reverse('blog:post', kwargs={'slug': item.slug})

    def item_author_name(self, item):
        return '%s' % (item.blog.user.username )

    def item_author_email(self, item):
        return item.blog.user.email

    def item_pubdate(self, item):
        return item.creation_date

def get_rss_interact(request, blog_id=None):
    blog = Blog.objects.get(pk=blog_id)
    title = blog.title

    link = reverse('blog:blog_posts', kwargs={'slug': blog.slug} )
    description = title
    items = []

    return HttpResponse(data_json, mimetype='application/json')
