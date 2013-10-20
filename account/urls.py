from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^$', 'my_account', name='my-account'),
    url(r'^domains/$', 'my_domains', name="my-domains"),
    url(r'^domains/(?P<id>\d+)/delete/$', 'delete_domain', name="delete-domain"),
    url(r'^forms/', include('concept.urls')),
    url(r'^messages/', include('concept.message_urls')),
    url(r'^plan/', include('plan.urls')),
    url(r'^password/$', 'my_password', name="my-password"),
    url(r'^close/$', 'close_account', name="close-account"),
)