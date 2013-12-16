from django.conf.urls import patterns,url
from blog import views

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^login/$',views.login_page, name='login'),
    url(r'^login_check/$',views.login_check, name='login_check'),
    url(r'^blog_posts/(?P<slug>[\d\w_-]+)/$',views.blog_posts, name='blog_posts'),
    url(r'^create_blog/(?P<username>.+)/$',views.create_blog, name='create_blog'),
)
