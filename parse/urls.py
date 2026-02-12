from django.urls import path
from . import views

urlpatterns = [
    path("buy/", views.p2p_buy_list),
    path("sell/", views.p2p_sell_list),
]
