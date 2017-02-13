from django.conf.urls import url
from searchapp import views

urlpatterns = [
    url(r'^search/$', views.search, name="search"),
    url(r'^dokumenti/$', views.static1, name="dokumenti"),
    url(r'^skenerdirektorija/$', views.static2, name="skenerdirektorija"),
]