from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^cuasalumnisite/', include('cuasalumnisite.foo.urls')),
    url(r'^$', 'cuasalumnisite.home.views.index', name='home_url'),
    url(r'^news/$', 'cuasalumnisite.news.views.articleList', name='news_url'),
    url(r'^news/(\d+)/$', 'cuasalumnisite.news.views.articleDetail', name='news_detail_url'),
    url(r'^events/', include('cuasalumnisite.events.urls')), 
    url(r'^about/$', direct_to_template, {'template': 'about/about.html'}, 'about_url'),
    url(r'^members/', include('cuasalumnisite.members.urls')),
    url(r'^signup/$', 'cuasalumnisite.members.views.signup', name='signup_url'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'home/login.html'}, 'login_url'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'redirect_field_name' : 'next'}, 'logout_url'),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEV:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.STATIC_DOC_ROOT})
    )
