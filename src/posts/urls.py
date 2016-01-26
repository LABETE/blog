from django.conf.urls import include, url
from django.contrib import admin

from .views import (
	PostCreateView,
	PostUpdateView,
	PostDetailView,
	PostListView,
	PostDeleteView)

urlpatterns = [
    url(r'^$', view=PostListView.as_view(), name="list"),
    url(r'^create/$', view=PostCreateView.as_view(), name="create"),
    url(r'^(?P<slug>[\w-]+)/$', view=PostDetailView.as_view(), name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', view=PostUpdateView.as_view(), name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', view=PostDeleteView.as_view(), name="delete"),
]
