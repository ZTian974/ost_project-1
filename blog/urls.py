from django.conf.urls import patterns,url
from blog import views

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^login/$',views.login_page, name='login_page'),
    url(r'^sign_up/$',views.sign_up,name='sign_up'),
    url(r'^blog_posts/(?P<slug>[\d\w_-]+)/$',views.blog_posts, name='blog_posts'),
    url(r'^post/(?P<slug>[\d\w_-]+)/$',views.post, name='post'),
    url(r'^edit_post/(?P<slug>[\d\w_-]+)/$',views.edit_post, name='edit_post'),
    url(r'^create_post/(?P<slug>[\d\w_-]+)/$',views.create_post, name='create_post'),
    url(r'^tag/(?P<slug>[\d\w_-]+)/$',views.tag, name='tag'),
    url(r'^create_blog/(?P<username>.+)/$',views.create_blog, name='create_blog'),
)