from django.conf.urls import patterns, url
from views import functions_list, execute, legend

urlpatterns = patterns('',
    # url(r'^list/', functions_list), # todo: is this necessary?
    url(r'^execute/(.+)', execute),
    url(r'^legend/(.+)', legend),
)
