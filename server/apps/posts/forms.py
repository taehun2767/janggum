from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'name', 'age']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'photo')