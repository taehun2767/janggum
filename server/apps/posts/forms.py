from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Post

class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'name', 'age']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'photo')

class CustomAuthenticationForm(AuthenticationForm):
   error_messages = {
      'invalid_login': (
        "비밀번호나 이메일이 올바르지 않습니다. 다시 확인해 주세요."
      ),
      "inactive": ("이 계정은 인증되지 않았습니다. 인증을 먼저 진행해 주세요."),
   }
   