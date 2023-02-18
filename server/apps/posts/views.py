from django.shortcuts import render, redirect, get_object_or_404
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post, Comment, Like, Comment
from django.http.request import HttpRequest
from django.db.models import Q

from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

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
                if posts.filter(ingredient__contains=ele):
                    posts = posts.filter(ingredient__contains=ele)
                    print(posts)
                else :
                    error= "재료가 포함된 요리가 없어요!"
                    context={
                    "error" : error, 
                    }
                    return render(request, "posts/main.html", context=context)
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
    
#프로필
def profile(request:HttpRequest, pk, *args, **kwargs):
    userName = User.objects.get(id=pk)
    print(userName)
    Posts = Post.objects.all().filter(user=userName)
    print(Posts[1].title)
    for post in Posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientList = ingredientStr.split(',')
                #새 필드 만들어서 html에 데이터 보냄
                post.ingredientList = ingredientList
                post.save()   
    context = {
        "posts" : Posts
    }
    return render(request,"posts/profile.html", context=context)

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
        #유효하지 않은 경우 redirect ()
        else:
            error = "에러"
            context = {
            'error' : error,
            }
            return render(request, "posts/signup.html", context=context)
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
    
    for post in posts:
        user_pk =User.objects.all().filter(name=post.user)
        if user_pk:
            user_pk= user_pk[0].pk
        post.user_pk = user_pk
        post.save()
    # 검색기능 주석처리함
    # text = request.GET.get("text")
    # if text:
    #     posts = posts.filter(content__contains=text)
    sort = request.GET.get('sort', '')
    if sort =="likes":
        posts = posts.order_by('-number', '-created_at')
    else:
        posts = posts.order_by('-created_at')
    if request.method == "POST":
        searchName = request.POST.get("search-name")
        posts = posts.filter(title__contains=searchName)
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
        "sortN" : sort
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
def posts_janggum_list(request:HttpRequest, *args, **kwargs):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    
    for post in posts:
        user_pk =User.objects.all().filter(name=post.user)
        if user_pk:
            user_pk= user_pk[0].pk
        post.user_pk = user_pk
        post.save()
    sort = request.GET.get('sort', '')
    if sort =="likes":
        posts = posts.order_by('-number', '-created_at')
    else:
        posts = posts.order_by('-created_at')
    if request.method == "POST":
        searchName = request.POST.get("search-name")
        posts = posts.filter(title__contains=searchName)
    for post in posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientList = ingredientStr.split(',')
                post.ingredientList = ingredientList
                post.save()
    context = {
        "posts" : posts,
        'comments' : comments,
        "sortN" : sort
    }
    return render(request, "posts/jangum_recipe_list.html", context=context)

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
            all_used_ingredient_set.add(ele.replace(" ",""))
        print(all_used_ingredient_set)
        Post.objects.create(
            ingredient = ingredients,
            user=request.user,
            title=request.POST["title"],
            photo=request.FILES['photo'],
            content=request.POST["content"],
            ingredient_quantity = request.POST["ingredient_quantity"],
        )
        return redirect("/")
    return render(request, "posts/recipe_create_page.html", context=context)

# update
def posts_update(request:HttpRequest, pk, *args, **kwargs):
    # filename = request.FILES.get("photo").name
    # print(filename)
    post = Post.objects.get(id=pk)
    #재료가 각각 표시되게끔 전처리

    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientList = ingredientStr.split(',')
    post.ingredientList = ingredientList
    post.save()
    if request.method == "POST":
        post.title=request.POST["title"]
        if request.FILES.get('photo') is not None:
            post.photo=request.FILES.get("photo")
        post.content=request.POST["content"]
        post.ingredient = request.POST.getlist('ingredient[]')
        post.ingredient_quantity = request.POST["ingredient_quantity"]
        post.save()
        for ele in post.ingredient[0]:
            all_used_ingredient_set.add(ele.replace(" ",""))
        print(all_used_ingredient_set)
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
        if post.user == User.objects.get(username= request.user.get_username()):
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

# @csrf_exempt #403에러 방지
# def detailajax(request, *args, **kwargs):
#     req = json.loads(request.body)

#     post_id = req['id']
#     post = Post.objects.get(id = post_id)
#     comments = Comment.objects.filter(post_id=post)
#     comment_id_L = []
#     comment_userid_L = []
#     comment_content_L = []
#     comment_created_L = []
#     # for comment in comments:
#     #     comment_id_L.append(comment.id)
#     #     comment_userid_L.append(comment.user_id)
#     #     comment_content_L.append(comment.content)
#     #     comment_created_L.append(comment.created_at)
#     post_title = post.title
#     photo_url = post.photo.url
#     ingredientStr = post.ingredient[2:-3].replace("'", '')
#     ingredientL = ingredientStr.split(',')
#     post_content = post.content
#     post_created = str(post.created_at).replace("-", '.')
    
#     data = {'post_id': post_id, 
#             'post_title':post_title, 
#             'post_content': post_content, 
#             'post_created':post_created,
#             'photo_url':photo_url,
#             'ingredientL':ingredientL,
#             'comments': comments}
    
#     return JsonResponse(data)



@csrf_exempt #403에러 방지
def detailajax(request, *args, **kwargs):
    req = json.loads(request.body)

    post_id = req['id']
    post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post_id=post)
    commentList = []
    comment_id_L = []
    comment_userid_L = []
    comment_content_L = []
    comment_created_L = []
    for comment in comments:
        comment_id_L.append(comment.id)
        comment_userid_L.append(comment.user_id.username)
        comment_content_L.append(comment.content)
        comment_created_L.append(comment.created_at)
        commentList.append(comment)
    
        
    post_title = post.title
    photo_url = post.photo.url
    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientL = ingredientStr.split(',')
    post_content = post.content
    post_created = str(post.created_at).replace("-", '.')
    commentList = list(comments.values())
    # commentList = zip(comment_id_L, comment_userid_L, comment_content_L, comment_created_L)
    # data ={
    #     'post_id': post_id,
    #     'post_title':post_title,
    #     'post_content': post_content, 
    #     'post_created':post_created,
    #     'photo_url':photo_url,
    #     'ingredientL':ingredientL,
    #     'comments': comments,
    # }


    return JsonResponse({'post_id': post_id, 'post_title':post_title,  'post_content': post_content, 'post_created':post_created, 'photo_url':photo_url, 'ingredientL':ingredientL, 'comments': commentList})
    # return JsonResponse({'post_id': post_id, 'post_title':post_title,  'post_content': post_content, 'post_created':post_created, 'photo_url':photo_url, 'ingredientL':ingredientL, 'comment_id_L':comment_id_L, 'comment_content_L':comment_content_L, 'comment_created_L':comment_created_L, 'comment_id_L':comment_id_L})
# 'comment_id_L':comment_id_L, 'comment_userid_L':comment_userid_L, 'comment_content_L':comment_content_L, 'comment_created_L':comment_created_L



# def comments_create(request:HttpRequest, pk, *args, **kwargs):
#     if request.user.is_authenticated:
#         post = get_object_or_404(Post, pk=pk)
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.post_id = post
#             comment.user_id = request.user
#             comment.save()
            

@csrf_exempt #403에러 방지
def comment_create(request, pk, *args, **kwargs):
    # req = json.loads(request.body)

    # post_id = req['id']
    # post = get_object_or_404(Post, id=post_id)
    # 수정전
    print(Post.objects.all())
    post = get_object_or_404(Post, id=pk)
    comment_writer = request.POST.get('comment_writer')
    user_id = User.objects.all().get(username=comment_writer)
    content = request.POST.get('content')
    if content:

        comment = Comment.objects.create(
            user_id = user_id,
            post_id = post,
            content = content,
        )
        post.save()
        comments = Comment.objects.all()
        data = {
            'comment_writer' : comment_writer,
            'content' : content,
            'created': '방금 전',
            'comment_id' : comment.id,
        }
        if request.user == post.user:
            data['self_comment'] = '(글쓴이)'


        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

@csrf_exempt #403에러 방지
def comment_delete(request, pk, *args, **kwargs):
    # req = json.loads(request.body)

    # post_id = req['id']
    # post = get_object_or_404(Post, id=post_id)
    
    # 수정 전
    post = get_object_or_404(Post, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)
    
    if request.user == target_comment.user_id:
        target_comment.delete()
        # target_comment.save()
        post.save()
        data = {
            'comment_id' : comment_id,
        }
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")
# @csrf_exempt #403에러 방지
# def comment_ajax(request, *args, **kwargs):
#     if request.user.is_authenticated:
#         req = json.loads(request.body)

#         postid = req['id']
#         userid = request.user
#         contents = req['content']
#         comment = Comment.objects.create(
#             post_id = Post.objects.get(id=postid),
#             user_id = Post.objects.get(id=userid),
#             content = contents
#         )
#         comment.save()

#     return JsonResponse({'post_id': postid, 'user_id':userid, 'comment_id': comment.pk, 'content': comment.content})

# @csrf_exempt
# def comment_del_ajax(request, *args, **kwargs):
#     req = json.loads(request.body)

#     post_id = req['post_id']
#     comment_id = req['comment_id']
#     comment = Comment.objects.get(id=comment_id)
#     comment.delete()
#     return JsonResponse({'post_id': post_id, 'comment_id': comment_id})


