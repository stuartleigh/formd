from django.conf.urls import patterns, include, url

urlpatterns = patterns('concept.views',
    url(r'^$', 'my_messages', name='my-messages'),
    url(r'^(?P<message_id>\w+)/$', 'view_message', name="view-message"),
)