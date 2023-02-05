from django.shortcuts import render, redirect
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post

def main(request):
    return render(request, "posts/main.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')   
            return render(request, template_name="posts/success.html")
        else:
            return redirect('posts:signup')
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='posts/signup.html', context=context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('posts:main')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='posts/login.html', context=context)
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, template_name='posts/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('posts:main')

def create(request):
    return render(request, "posts/recipe_create_page.html")

def all_recipe(request):
    recipe = Post.objects.all()
    context = {
                'recipe': recipe,
            }
    return render(request, "posts/all_recipe_list.html", context=context)