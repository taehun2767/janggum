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
    path('posts/store_recipe_list', views.store_recipe_list, name='store_recipe_list'),
    path('posts/posts_janggum_list', views.posts_janggum_list, name='posts_janggum_list'),
    path('posts/<int:pk>/update', views.posts_update, name='update'),
    path('posts/<int:pk>/delete', views.posts_delete, name='delete'),
    path('posts/<int:pk>', views.posts_retrieve, name='retrieve'),
    path('detail_ajax/', views.detailajax, name='detail_ajax'),
    path('store_ajax/', views.store_ajax, name='store_ajax'),
    path('like_ajax/', views.like_ajax, name='like_ajax'),
    path('comment/<int:pk>/create/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # path('posts/<int:pk>/comments', views.comments_create, name='comments_create'),
    # path('posts/<int:post_pk>/comments/<int:comment_pk>/delete', views.comments_delete, name='comments_delete'),
]