from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^wpsoutputs/(?P<file_name>pywps-.*?\.xml)$', views.get_status_report,
        name='get_status_report'),
)
