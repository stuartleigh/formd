from django.conf.urls import patterns, include, url

urlpatterns = patterns('plan.views',
    url(r'^$', 'my_plan', name="my-plan"),
    url(r'^declined/$', 'card_declined', name="card-declined"),
)