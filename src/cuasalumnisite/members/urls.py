from django.conf.urls.defaults import *

urlpatterns = patterns('cuasalumnisite.members.views',
    url(r'^payment/$', 'payment', name='payment_url'),
    url(r'^payment/complete/$', 'payment_complete', name='payment_complete_url'),
    url(r'^payment/cancelled/$', 'payment_cancelled', name='payment_cancel_url'),
    url(r'^account/$', 'account', name='your_account_url'),
    )

urlpatterns += patterns('',
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', {'template_name': 'members/password_reset_form.html', 'email_template_name': 'members/password_email_template.html'}, 'reset_password_url'),
    url(r'^reset_password_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'members/password_reset_done.html'}),
    url(r'^reset_password_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'members/password_reset_confirm.html'}, 'reset_password_confirm'),
    url(r'^reset_password_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'members/password_reset_complete.html'}),
                 
)