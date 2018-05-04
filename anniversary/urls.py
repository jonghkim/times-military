from django.conf.urls import url
from . import views

app_name = 'anniversary'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^anniversary/$', views.anniversary, name='anniversary'),
    url(r'^restaurant/$', views.restaurant_func, name='restaurant'),
    url(r'^restaurant/new/$', views.post_new, name='post_new'),
    url(r'^restaurant/vote/$', views.vote, name='vote'),
    url(r'^restaurant/vote/result/(?P<rest_id>\d+)/$', views.rating, name='rating'),
    url(r'^restaurant/vote/(?P<name>[\w|\W]+)/$', views.vote, name='vote'),
    url(r'^wallet/$', views.wallet, name='wallet'),
    url(r'^about/$', views.about, name='about'),
    url(r'^devideas/$', views.devideas, name='devideas'),

]
