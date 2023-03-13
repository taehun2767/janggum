from django.db import models
from django.contrib.auth.models import AbstractUser

#지금까지 기록한 재료들  => textfield로 생성 후 view.py에서 json으로 처리하여 리스트화 
class AllUsedIngredient(models.Model):
  all_ingreident = models.TextField(null=True)

#유저
class User(AbstractUser):
    name = models.CharField(max_length=30, verbose_name="닉네임")
    member_id = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    age = models.IntegerField(null=True, verbose_name="나이")
    username = models.CharField(verbose_name="아이디", unique=True, max_length=30)


#게시글
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    photo = models.ImageField(blank=True, upload_to='posts/%Y%m%d', default='default.png')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredient = models.TextField()
    ingredient_quantity = models.TextField(default="")
    number = models.IntegerField(default=0)
    
#댓글
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#좋아요
class Like(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")
  like_value = models.BooleanField(default=False)

class Store(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store_user")
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="store_post")
  store_value = models.BooleanField(default=False)
  
