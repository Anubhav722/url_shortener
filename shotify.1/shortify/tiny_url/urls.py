from django.conf.urls import url, include
from tiny_url import views


urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^shorten/', views.short, name='shorten'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^shorten/(?P<short>[0-9]+[a-z]+[A-Z]+)/$', views.redirect_short_url, name='redirect_short_url'),
]