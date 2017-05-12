from django.conf.urls import url

from .views import Index, Post1

urlpatterns = [
    url(r'^$', Index.as_view(), name='home'),
    url(r'^posts/(?P<title>[-\w]+)/$', Post1.as_view(), name='posts1'),

]
