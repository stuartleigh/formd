from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v0/message/$', 'concept.views.message_api', name='message-api'),
    url(r'^api/v0/message/received/$', 'concept.views.message_received', name="message-received"),

    url(r'^my-account/', include('account.urls')),

    url(r'^sign-up/$', 'account.views.sign_up', name='sign-up'),
    url(r'^log-in/$', 'account.views.log_in', name='log-in'),
    url(r'^logout/$', 'account.views.log_out', name='logout'),

    url(r'^$', 'formd.views.homepage', name='homepage'),
    url(r'^getting-started/$', 'formd.views.getting_started', name='getting-started'),

    url(r'^queue/', include('django_rq.urls')),
)