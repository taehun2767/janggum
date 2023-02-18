from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment

class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'name', 'age']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'photo')
        
# class CommentForm(forms.ModelForm):
#   class Meta:
#     model = Comment
#     exclude = ('user_id', 'post_id',)