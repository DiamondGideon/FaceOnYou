from django.conf.urls import url
from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all$', views.index_all, name='index_all'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^(?P<post_id>[0-9]+)/create_coment/$', views.create_coment, name='create_coment'),
    url(r'^(?P<post_id>[0-9]+)/favorite_post/$', views.favorite_post, name='favorite_post'),
    url(r'^(?P<post_id>[0-9]+)/delete_post/$', views.delete_post, name='delete_post'),
]
