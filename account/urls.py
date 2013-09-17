from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^$', 'my_account', name='my-account'),
    url(r'^forms/', include('concept.urls')),
    url(r'^messages/', include('concept.message_urls')),
    url(r'^plan/$', 'my_plan', name="my-plan"),
    url(r'^password/$', 'my_password', name="my-password"),
)