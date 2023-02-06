from django.urls import path, include
from . import views


app_name = "posts"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path('accounts/', include('allauth.urls')),
    
    path('posts/create', views.create, name='create'),
    path('posts/all_recipe', views.posts_all_list, name='all_recipe'),
    path('posts/<int:pk>/update', views.posts_update, name='update'),
    path('posts/<int:pk>/delete', views.posts_delete, name='delete'),
]