from django.shortcuts import render, redirect
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post, Comment

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

from .forms import PostForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt #보안 관련 부분

@csrf_exempt
def like_ajax(request, *args, **kwargs):
    req = json.loads(request.body)

    post_id = req['id']
    post = Post.objects.get(id = post_id)

    if post.like == True:
        post.like = False
    else:
        post.like = True
    post.save()

    liked = post.like
    return JsonResponse({'id': post_id, 'liked': liked})

@csrf_exempt #403에러 방지
def comment_ajax(request, *args, **kwargs):
    req = json.loads(request.body) #{id:1, content: ...}

    post_id = req['id'] #1
    content = req['content'] #...

    comment = Comment.objects.create(
        post = Post.objects.get(id=post_id),
        content = content,
    )

    return JsonResponse({'post_id': post_id, 'comment_id': comment.id, 'content': comment.content})

@csrf_exempt
def comment_del_ajax(request, *args, **kwargs):
    req = json.loads(request.body)

    post_id = req['post_id']
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'post_id': post_id, 'comment_id': comment_id})