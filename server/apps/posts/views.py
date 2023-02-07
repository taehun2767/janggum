from django.shortcuts import render, redirect
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post, Comment, Like, Comment
from django.http.request import HttpRequest
from django.db.models import Q


all_used_ingredient_set = set()

#메인 페이지 => main.html을 기본으로 보여주고 재료로 검색시 recipe list 창으로 context 보내며 render
def main(request):
    #레시피 검색 시 context 넘겨주기 위한 작업
    posts = Post.objects.all()
    if request.method == "POST":
        ingredientList = request.POST.getlist("search")
        print(ingredientList)
        #각각 검색재료에 대해 필터링
        for ele in ingredientList:
            if ele:
                posts = posts.filter(ingredient__contains=ele)
                print(posts)
        #해당조건의 레시피가 존재할 때
        if posts:
            #재료를 파이썬 리스트화해야 전체 레시피 보기에서 재료도 보이게 할 수 있음
            ingredientLists = []
            for post in posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientList = ingredientStr.split(',')
                #약간 야매인 거 같긴한데 새로운 field만들어서 파이썬 리스트 추가
                post.ingredientList = ingredientList
                post.save()
            context={
                "posts" : posts,
            }
        #검색한 경우 레시피 리스트 페이지로 render
        return render(request, "posts/all_recipe_list.html", context=context)
    #검색을 하지 않을 경우 main으로 render
    return render(request, "posts/main.html")


#회원가입
def signup(request):
    #form 입력 후 제출
    if request.method == 'POST':
        form = SignupForm(request.POST)
        #form이 유효한 경우
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')   
            return render(request, template_name="posts/success.html")
        #유효하지 않은 경우 redirect
        else:
            return redirect('posts:signup')
    #기본으로 띄우는 창
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='posts/signup.html', context=context)

#로그인 페이지
def login(request):
    #아이디 비밀번호 입력 후 제출
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
    #제출 아닌 경우 로그인 페이지 그대로
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, template_name='posts/login.html', context=context)

#로그아웃 시 메인 페이지로 이동
def logout(request):
    auth.logout(request)
    return redirect('posts:main')

# all_recipe_list페이지 
def posts_all_list(request:HttpRequest, *args, **kwargs):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    # 검색기능 주석처리함
    # text = request.GET.get("text")
    # if text:
    #     posts = posts.filter(content__contains=text)
    
    #데이터 전처리 => 재료가 textfield로 저장되어있으므로 각 재료를 창에 띄울 수 있도록 리스트화
    for post in posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientList = ingredientStr.split(',')
                #새 필드 만들어서 html에 데이터 보냄
                post.ingredientList = ingredientList
                post.save()   
    context = {
        "posts" : posts,
        'comments' : comments,
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
    comments = Comment.objects.all()
    context = {
        "posts" : posts,
        'comments' : comments,
    }
    return render(request, "posts/jungum_recipe_list.html", context=context)

# create page
def create(request:HttpRequest, *args, **kwargs):

    context = {
        "ingredientList" : all_used_ingredient_set,
    }
    if request.method == "POST":
        #여러 재료 input들 한꺼번에 가져와 저장
        ingredients = request.POST.getlist('ingredient[]'),
        print(ingredients)
        ingredientList = ingredients[0]
        for ele in ingredientList:
            all_used_ingredient_set.add(ele)
        Post.objects.create(
            ingredient = ingredients,
            user=request.user,
            title=request.POST["title"],
            photo=request.FILES['photo'],
            content=request.POST["content"],
        )
        return redirect("/")
    return render(request, "posts/recipe_create_page.html", context=context)

# update
def posts_update(request:HttpRequest, pk, *args, **kwargs):
    
    post = Post.objects.get(id=pk)
    #재료가 각각 표시되게끔 전처리
    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientList = ingredientStr.split(',')
    post.ingredientList = ingredientList
    post.save()
    if request.method == "POST":
        post.title=request.POST["title"]
        post.photo=request.FILES["photo"]
        post.content=request.POST["content"]
        post.ingredient = request.POST.getlist('ingredient[]'),
        post.save()
        

        for ele in post.ingredient[0]:
            all_used_ingredient_set.add(ele)
        return redirect(f"/")
    #수정 페이지에 원래 레시피 정보 뜨게끔 context로 보냄
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

def posts_retrieve(request:HttpRequest, pk, *args, **kwargs):
    post = Post.objects.all().get(id=pk)
    
    #데이터 전처리 string -> list
    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientList = ingredientStr.split(',')
    print(ingredientList)
    context = {
        "post" : post,
        "ingredient" : ingredientList,
    }
    return render(request, "posts/recipe_search_page_list.html", context=context)

from .forms import PostForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def like_ajax(request, *args, **kwargs):
    if request.user.is_authenticated:
        req = json.loads(request.body)
        user = request.user
        like_id = req['id']
        post = Post.objects.get(id=like_id)
        like = Like.objects.filter(post_id=post, user_id=user)
        like_true = True

        if like.exists(): 
            like.delete()
            post.number -= 1
            post.save()
            like_true = False
            return JsonResponse({'like_true': like_true, 'number': post.number})
        
        Like.objects.create(
            post_id = post,
            user_id = user,
            like_value = True,
            
        )
        post.number += 1
        post.save()
            

    return JsonResponse({'like_true': like_true, 'number': post.number})

@csrf_exempt #403에러 방지
def detailajax(request, *args, **kwargs):
    req = json.loads(request.body)

    post_id = req['id']
    post = Post.objects.get(id = post_id)
    post_title = post.title
    # post_photo = post.photo
    post_content = post.content
    post_created = post.created_at

    return JsonResponse({'post_id': post_id, 'post_title':post_title, 'post_content': post_content, 'post_created':post_created})

@csrf_exempt #403에러 방지
def comment_ajax(request, *args, **kwargs):
    req = json.loads(request.body)

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


