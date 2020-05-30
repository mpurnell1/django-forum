"""django_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views

app_name = 'forumapp'
urlpatterns = [
<<<<<<< HEAD
        url(r'^(?P<channel>[-\w]+)/(?P<thread>[0-9]+)/$', views.CommentView.as_view(), name='comment'),
    url(r'^(?P<channel>[-\w]+)/', views.ThreadView.as_view(), name='thread'),
=======
    url(r'^channel/(?P<channel_name>[-\w]+)/(?P<thread_id>[0-9]+)/$', views.CommentView.as_view(), name='comment'),
    url(r'^channel/(?P<channel_name>[-\w]+)/$', views.ThreadView.as_view(), name='thread'),
>>>>>>> 172c47f0b43b476d321469db7d82504470c8b422
    url(r'^$', views.ChannelView.as_view(), name='channel'),
]
