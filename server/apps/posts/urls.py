from django.urls import path, include
from . import views


app_name = "posts"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path('accounts/', include('allauth.urls')),
    path('profile/<int:pk>', views.profile, name='profile'),
    
    path('posts/create', views.create, name='create'),
    path('posts/all_recipe', views.posts_all_list, name='all_recipe'),
    path('posts/<int:pk>/update', views.posts_update, name='update'),
    path('posts/<int:pk>/delete', views.posts_delete, name='delete'),
    path('posts/<int:pk>', views.posts_retrieve, name='retrieve'),
    path('detail_ajax/', views.detailajax, name='detail_ajax'),
    path('like_ajax/', views.like_ajax, name='like_ajax'),
    path('comment_ajax/', views.comment_ajax, name='comment_ajax'),
    path('comment_del_ajax/', views.comment_del_ajax, name='comment_del_ajax'),
]