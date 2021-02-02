from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^commodity_list', views.commodity_list),
    url(r'^recharge', views.recharge),
]