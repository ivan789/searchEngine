from django.conf.urls import url
from searchapp import views

urlpatterns = [
    url(r'^$', views.search, name="index"),
    url(r'^dokumenti/$', views.static1, name="dokumenti"),
    url(r'^skenerdirektorija/$', views.static2, name="skenerdirektorija"),
]
