# healthwebUI/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('redirect_login/',views.redirect_login,name="redirect_login"),
    path('find-doctor/', views.find_doctor, name='find_doctor'),
]