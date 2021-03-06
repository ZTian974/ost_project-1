from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ost_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/',include('blog.urls',namespace='blog')),
)+ static (settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
