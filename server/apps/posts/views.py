from django.shortcuts import render, redirect
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post, Comment
from django.http.request import HttpRequest

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

# all_recipe_list페이지 
def posts_all_list(request:HttpRequest, *args, **kwargs):
    posts = Post.objects.all()
    # 검색기능 주석처리함
    # text = request.GET.get("text")
    # if text:
    #     posts = posts.filter(content__contains=text)        
    context = {
        "posts" : posts,
    }
    return render(request, "posts/all_recipe_list.html", context=context)

# recipe search page 선택값으로 찾는거 구현 안함
# def posts_search_list(request:HttpRequest, *args, **kwargs):
#     posts = Post.objects.all()
   
#     context = {
#         "posts" : posts,
#     }
#     return render(request, "posts/recipe_search_page_list.html", context=context)

# 장금이 레시피 페이지 일단 좋아요 없이 구현
def posts_junggum_list(request:HttpRequest, *args, **kwargs):
    posts = Post.objects.all()
       
    context = {
        "posts" : posts,
    }
    return render(request, "posts/jungum_recipe_list.html", context=context)

# create page
def create(request:HttpRequest, *args, **kwargs):
    if request.method == "POST":
        # ingredientList = []
        # for i in range(1, 4):
        #     temp = request.POST.get(f"ingredient{i}")
        #     ingredientList.append(temp)
        # ingredientList
        # print(ingredientList)
        ingredients = request.POST.getlist('ingredient[]'),
        print(ingredients)
        Post.objects.create(
            ingredient = ingredients,
            user=request.user,
            title=request.POST["title"],
            photo=request.FILES['photo'],
            content=request.POST["content"],
        )
        return redirect("/")
    return render(request, "posts/recipe_create_page.html")

# update
def posts_update(request:HttpRequest, pk, *args, **kwargs):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.title=request.POST["title"]
        post.photo=request.FILES["photo"]
        post.content=request.POST["content"]
        post.save()
        return redirect(f"/")
    context = {
        "post" : post,
    }
    return render(request, "posts/recipe_update_page.html", context=context)

# delete 
def posts_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()
    return redirect("posts:all_recipe")

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

