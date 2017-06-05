from django.conf.urls import url

from .views import Index, PostView, PostsList

urlpatterns = [
    url(r'^$', Index.as_view(), name='home'),
    url(r'^posts/(?P<index_url>[-\w]+)/$', PostView.as_view()),
    url(r'^posts/page/(?P<page>\d+)/$', PostsList.as_view()),

]
