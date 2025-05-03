from django.urls import path
from . import views

urlpatterns = [
    path('', views.onboarding, name='onboarding'),  # new landing page
    path('home/', views.home, name='home'),  # moved home view
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]