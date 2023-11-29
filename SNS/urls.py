from django.urls import path
from app import views

urlpatterns = [
    path('index/', views.index),
    path('connection/', views.connection),
    path('profile/', views.profile),
    path('sign-in/', views.sign_in),
    path('sign-up/', views.sign_up),
    path('index/comment/', views.comment),
    path('index/follow/', views.follow),
    path('index/transaction/', views.transfer),
    path('logout/', views.logout),
    path('code/', views.code),
]
