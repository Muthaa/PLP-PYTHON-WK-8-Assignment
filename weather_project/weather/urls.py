from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('signup/', views.signup_view, name='signup'),
    path('save/', views.save_favorite, name='save_favorite'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

]
