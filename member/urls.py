from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^member_list', views.users_list)
]
