from django.conf.urls import patterns, include, url

urlpatterns = patterns('plan.views',
    url(r'^$', 'my_plan', name="my-plan"),
)