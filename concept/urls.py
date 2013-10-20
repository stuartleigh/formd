from django.conf.urls import patterns, include, url

urlpatterns = patterns('concept.views',
    url(r'^$', 'my_concepts', name='my-concepts'),
    url(r'^new/$', 'new_concept', name='new-concept'),
    url(r'^(?P<concept_code>\w+)/$', 'view_concept', name="view-concept"),
)