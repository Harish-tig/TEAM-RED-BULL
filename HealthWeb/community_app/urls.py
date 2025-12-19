from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('journey/add/', views.add_journey, name='add_journey'),
    path('question/<int:question_id>/upvote/', views.upvote_question, name='upvote_question'),
    path('answer/<int:answer_id>/upvote/', views.upvote_answer, name='upvote_answer'),
]