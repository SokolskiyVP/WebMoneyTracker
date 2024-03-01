from django.urls import path
from . import views

urlpatterns = [
    path('',views.tinkoffapp, name='tinkoffapp'),
    path('shares/',views.render_tinkoff_shares, name='shares'),
    path('bonds/',views.render_tinkoff_bonds, name='bonds'),
    path('etf/',views.render_tinkoff_etf, name='etf'),
    path('currency/',views.render_tinkoff_curr, name='currency'),
]