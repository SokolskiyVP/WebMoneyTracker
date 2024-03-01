from django.urls import path
from . import views
from users import views as usersviews


urlpatterns = [
    path('',views.home, name='home'),
    path('login/', usersviews.login_user, name = 'login'),
    path('ChoosePortfolio/', views.ChoosePortfolio, name = 'ChoosePortfolio'),


]