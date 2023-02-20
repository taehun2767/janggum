from django.shortcuts import render, redirect, get_object_or_404
from server.apps.posts.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Post, Comment, Like, Comment, AllUsedIngredient, Store
from django.http.request import HttpRequest
from django.db.models import Q

from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #페이지네이션
from datetime import datetime

all_used_ingredient_set = set()
ingredientL = []
#메인 페이지 => main.html을 기본으로 보여주고 재료로 검색시 recipe list 창으로 context 보내며 render
def main(request):
    #레시피 검색 시 context 넘겨주기 위한 작업
    global ingredientL
    posts = Post.objects.all()
    posts.delete
    postList = []

    if request.GET.get('page'):
        print(request.GET.get('page'))
        print(postList)
        print(ingredientL)
        for post in posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                
                usedIngredientList = ingredientStr.split(',')
                print(usedIngredientList,"사용한 재료")
                flag = True
                for ele in ingredientL:
                    print(ele, "검색 재료")
                    if ele: 
                        if ele not in usedIngredientList:
                            flag = False
                            break
                if flag:
                    postList.append(post)
        print(postList)
        if postList:
            print(postList[0].ingredient)
        #각각 검색재료에 대해 필터링
        # for ele in ingredientList:
        #     if ele:
        #         if posts.filter(ingredient__contains=ele):
        #             posts = posts.filter(ingredient__contains=ele)
        #             print(posts)    
        #         else :
        #             error= "재료가 포함된 요리가 없어요!"
        #             context={
        #             "error" : error, 
        #             }
        #             return render(request, "posts/main.html", context=context)
        
        # context={"posts" : postList}
        #해당조건의 레시피가 존재할 때
        if postList:
            #재료를 파이썬 리스트화해야 전체 레시피 보기에서 재료도 보이게 할 수 있음
            ingredientLists = []
            for post in postList:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientStr = ingredientStr.replace(" ", "")
                ingredientLists = ingredientStr.split(',')
                
                #약간 야매인 거 같긴한데 새로운 field만들어서 파이썬 리스트 추가
                post.ingredientList = ingredientLists
                post.save()

            # 페이지네이션
            page = request.GET.get('page')
            paginator = Paginator(postList, 12)

            # print(page_obj)
            # print(type(page_obj))
            # for ele in page_obj:
            #     print(ele)
            
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                page = paginator.num_pages
                page_obj = paginator.page(page)
                
            leftIndex = (int(page) - 2)
            if leftIndex < 1:
                leftIndex = 1
            
            rightIndex = (int(page) + 2)
            
            if rightIndex > paginator.num_pages:
                rightIndex = paginator.num_pages
            custom_range = range(leftIndex, rightIndex + 1)

            flag = True
            context = {
                "posts" : postList,
                "page_obj" : page_obj,
                "paginator" : paginator,
                'custom_range' : custom_range,
            }
            
            return render(request, "posts/all_recipe_list.html", context=context)
    if request.method == "POST":
        ingredientLtemp = request.POST.getlist("search")
        ingredientL = []
        for ele in ingredientLtemp:
            ele = ele.replace(" ", "")
            ingredientL.append(ele)

        for post in posts:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientStr = ingredientStr.replace(" ", "")
                usedIngredientList = ingredientStr.split(',')
                print(usedIngredientList,"사용한 재료")
                flag = True
                for ele in ingredientL:
                    print(ele, "검색 재료")
                    if ele: 
                        if ele not in usedIngredientList:
                            flag = False
                            break
                if flag:
                    postList.append(post)
        print(postList)
        if postList:
            print(postList[0].ingredient)
        #각각 검색재료에 대해 필터링
        # for ele in ingredientList:
        #     if ele:
        #         if posts.filter(ingredient__contains=ele):
        #             posts = posts.filter(ingredient__contains=ele)
        #             print(posts)    
        #         else :
        #             error= "재료가 포함된 요리가 없어요!"
        #             context={
        #             "error" : error, 
        #             }
        #             return render(request, "posts/main.html", context=context)
        
        # context={"posts" : postList}
        #해당조건의 레시피가 존재할 때
        if postList:
            #재료를 파이썬 리스트화해야 전체 레시피 보기에서 재료도 보이게 할 수 있음
            ingredientLists = []
            for post in postList:
                ingredientStr = post.ingredient[2:-3].replace("'", '')
                ingredientStr = ingredientStr.replace(" ", "")
                ingredientLists = ingredientStr.split(',')
                #약간 야매인 거 같긴한데 새로운 field만들어서 파이썬 리스트 추가
                post.ingredientList = ingredientLists
                post.save()

            # 페이지네이션
            page = 1
            paginator = Paginator(postList, 12)

            # print(page_obj)
            # print(type(page_obj))
            # for ele in page_obj:
            #     print(ele)
            
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                page = paginator.num_pages
                page_obj = paginator.page(page)
                
            leftIndex = (int(page) - 2)
            if leftIndex < 1:
                leftIndex = 1
            
            rightIndex = (int(page) + 2)
            
            if rightIndex > paginator.num_pages:
                rightIndex = paginator.num_pages
            custom_range = range(leftIndex, rightIndex + 1)

            flag = True
            context = {
                "posts" : postList,
                "page_obj" : page_obj,
                "paginator" : paginator,
                'custom_range' : custom_range,
            }
            
            return render(request, "posts/all_recipe_list.html", context=context)
        else:
            error= "재료가 포함된 요리가 없어요!"
            context={
            "error" : error, 
            }
            return render(request, "posts/main.html", context=context)
    #검색을 하지 않을 경우 main으로 render
    return render(request, "posts/main.html")
    
#프로필
def profile(request:HttpRequest, pk, *args, **kwargs):
    userName = User.objects.get(id=pk)
    # print(userName)/
    Posts = Post.objects.all().filter(user=userName)
    # print(Posts[1].title)
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
    # comments = Comment.objects.all()
    
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
                
    # 페이지네이션
    page = request.GET.get('page') #html에 get 넣어야함
    
    paginator = Paginator(posts, 12)

    # print(page_obj)
    # print(type(page_obj))
    # for ele in page_obj:
    #     print(ele)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
        
    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages
    custom_range = range(leftIndex, rightIndex + 1)

    context = {
        # 'sorted' : sort,
        "posts" : posts,
        # 'comments' : comments,
        "sortN" : sort,
        "page_obj" : page_obj,
        "paginator" : paginator,
        'custom_range' : custom_range,
    }
    return render(request, "posts/all_recipe_list.html", context=context)

def store_recipe_list(request:HttpRequest, *args, **kwargs):
    stores = Store.objects.filter(user_id = request.user)
    comments = Comment.objects.all()
    posts = []
    for store in stores:
        if store.store_value == True:
            posts.append(store.post_id)
    for post in posts:
        user_pk =User.objects.all().filter(name=post.user)
        if user_pk:
            user_pk= user_pk[0].pk
        post.user_pk = user_pk
        post.save()
    # sort = request.GET.get('sort', '')
    # if sort =="likes":
    #     posts = posts.order_by('-number', '-created_at')
    # else:
    #     posts = posts.order_by('-created_at')
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
    }
    return render(request, "posts/store_recipe.html", context=context)

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
    # context = {
    #     "posts" : posts,
    #     'comments' : comments,
    #     "sortN" : sort
    # }
    
    # 페이지네이션
    page = request.GET.get('page')
    paginator = Paginator(posts, 12)

    # print(page_obj)
    # print(type(page_obj))
    # for ele in page_obj:
    #     print(ele)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
        
    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages
    custom_range = range(leftIndex, rightIndex + 1)


    context = {
        "posts" : posts,
        "page_obj" : page_obj,
        "paginator" : paginator,
        'custom_range' : custom_range,
        "sortN" : sort,
    }
    
    return render(request, "posts/jangum_recipe_list.html", context=context)


# create page
def create(request:HttpRequest, *args, **kwargs):
    global all_used_ingredient_set
    if AllUsedIngredient.objects.all():
        used_ingredients = AllUsedIngredient.objects.all()[0]
        allUsedIngredientStr = used_ingredients.all_ingreident[1:-2].replace("'", '')
        allUsedIngredientList = allUsedIngredientStr.split(',')
        all_used_ingredient_set = set(allUsedIngredientList)
    context = {
        "ingredientList" : all_used_ingredient_set,
    }
    if request.method == "POST":
        #여러 재료 input들 한꺼번에 가져와 저장
        ingredients = request.POST.getlist('ingredient[]'),
        #print(ingredients)
        ingredientList = ingredients[0]
        for ele in ingredientList:
            all_used_ingredient_set.add(ele.replace(" ",""))
            
        if not AllUsedIngredient.objects.all():
            for ele in ingredientList:
                all_used_ingredient_set.add(ele.replace(" ",""))
            AllUsedIngredient.objects.create(
                all_ingreident = all_used_ingredient_set
            )
        else:

            used_ingredients = AllUsedIngredient.objects.all()[0]
            allUsedIngredientStr = used_ingredients.all_ingreident[1:-2].replace("'", '')
            allUsedIngredientList = allUsedIngredientStr.split(',')
            all_used_ingredient_set = set(allUsedIngredientList)

            for ele in ingredientList:
                #print(ele)
                all_used_ingredient_set.add(ele.replace(" ",""))

            used_ingredients.all_ingreident = all_used_ingredient_set
            #print(all_used_ingredient_set)
            #print(used_ingredients.all_ingreident)
            used_ingredients.save()


        # 대체 이미지 넣을 셰도 코드
        # if request.FILES.get('photo'):
        #     Post.objects.create(
        #         ingredient = ingredients,
        #         user=request.user,
        #         title=request.POST["title"],
        #         photo=request.FILES.get('photo'),
        #         content=request.POST["content"],
        #         ingredient_quantity = request.POST["ingredient_quantity"],
        #     )
        # else:
        #     Post.objects.create(
        #         ingredient = ingredients,
        #         user=request.user,
        #         title=request.POST["title"],
        #         photo= #민지가 만든 대체 이미지를 넣으면 될 거 같은데?
        #         content=request.POST["content"],
        #         ingredient_quantity = request.POST["ingredient_quantity"],
        #     )
            
    
        Post.objects.create(
            ingredient = ingredients,
            user=request.user,
            title=request.POST["title"],
            photo=request.FILES.get('photo'),
            content=request.POST["content"],
            ingredient_quantity = request.POST["ingredient_quantity"],
        )
        return redirect("/")
    return render(request, "posts/recipe_create_page.html", context=context)

# update
def posts_update(request:HttpRequest, pk, *args, **kwargs):
    global all_used_ingredient_set
    if AllUsedIngredient.objects.all():
        used_ingredients = AllUsedIngredient.objects.all()[0]
        allUsedIngredientStr = used_ingredients.all_ingreident[1:-2].replace("'", '')
        allUsedIngredientList = allUsedIngredientStr.split(',')
        all_used_ingredient_set = set(allUsedIngredientList)

    # filename = request.FILES.get("photo").name
    # print(filename)
    post = Post.objects.get(id=pk)
    #재료가 각각 표시되게끔 전처리
    photo_url = post.photo.url
    print(photo_url)
    
    for i in reversed(range(len(photo_url))):
        if photo_url[i] == "/":
            photo_url = photo_url[i+1:]
            break
    ingredients = request.POST.getlist('ingredient[]')
    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientList = ingredientStr.split(',')
    post.ingredientList = ingredientList
    post.save()
    if request.method == "POST":
        post.title=request.POST["title"]
        if request.FILES.get('photo') is not None:
            post.photo=request.FILES.get("photo")
        post.content=request.POST["content"]
        post.ingredient = ingredients
        post.ingredient_quantity = request.POST["ingredient_quantity"]
        post.save()
        
        # print(all_used_ingredient_set, "있던 set 가져오기")
        # print(post.ingredient)
        for ele in post.ingredient[0]:
            # print(ele)
            all_used_ingredient_set.add(ele.replace(" ",""))
        used_ingredients.all_ingreident = all_used_ingredient_set
        used_ingredients.save()
        # print(used_ingredients.all_ingreident, "새 db")
        # print(all_used_ingredient_set, "새 set")
        return redirect(f"/")
    #수정 페이지에 원래 레시피 정보 뜨게끔 context로 보냄
    post.all_used_ingredient_set = all_used_ingredient_set
    post.save()
    context = {
        "post" : post,
        "photo_url" : photo_url,
        "ingredientList" : all_used_ingredient_set,
    }
    #print(all_used_ingredient_set)
    # print(AllUsedIngredient.all_ingreident)/
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
    #print(ingredientList)
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
def store_ajax(request, *args, **kwargs):
    req = json.loads(request.body)
    store_id = req['id']
    store = Store.objects.filter(post_id=store_id, user_id=request.user)
    store_true = True
    if not store.exists():
        Store.objects.create(
            post_id = Post.objects.get(id=store_id),
            user_id = request.user,
            store_value = True
        )
        store_true = True
    else:
        store = Store.objects.get(post_id=store_id, user_id=request.user)
        if store.store_value == True:
            store.store_value = False
            store.save()
        else:
            store.store_value = True
            store.save()
        store_true = store.store_value
    return JsonResponse({'id':store_id, 'store_true': store_true})

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
            like = Like.objects.get(post_id=post, user_id=user)
            if like.like_value == True:
                like.like_value = False
                like.post_id.number -= 1
                like_true = False
            else:
                like.like_value = True
                like.post_id.number += 1
                like_true = True
            like.post_id.save()
            like.save()
            return JsonResponse({'id':like_id,'like_true': like_true, 'number': post.number})
        
        Like.objects.create(
            post_id = post,
            user_id = user,
            like_value = True,
        )
        post.number += 1
        post.save()

    return JsonResponse({'id':like_id, 'like_true': like_true, 'number': post.number})



@csrf_exempt #403에러 방지
def detailajax(request, *args, **kwargs):
    req = json.loads(request.body)

    post_id = req['id']

    post = Post.objects.get(id = post_id)

    comments = Comment.objects.filter(post_id=post)

    commentList = []
    # comment_id_L = []
    # comment_userid_L = []
    # comment_content_L = []
    # comment_created_L = []
    # for comment in comments:
    #     comment_id_L.append(comment.id)
    #     comment_userid_L.append(comment.user_id.username)
    #     comment_content_L.append(comment.content)
    #     comment_created_L.append(comment.created_at)

    post_username = post.user.username
    post_user = post.user.name
    post_title = post.title
    post_quantity = post.ingredient_quantity
    photo_url = post.photo.url
    print(photo_url, "photo url")
    ingredientStr = post.ingredient[2:-3].replace("'", '')
    ingredientL = ingredientStr.split(',')
    post_content = post.content
    post_created = str(post.created_at).replace("-", '.')
    # print()
    # print("코멘트 밸류", comments.values())
    commentList = list(comments.values(
        'id',
        'user_id__username',
        'user_id__name',
        'post_id',
        'content',
        'created_at',
        'updated_at',
    ))

    todayObject = datetime.today()
    today = ""
    today += str(todayObject.year).zfill(2)+"."+str(todayObject.month).zfill(2)+"."+str(todayObject.day).zfill(2)
    print("today", today)
    # print("오늘 날짜", today)
    for ele in commentList:
        time = ""
        hour = ele['created_at'].hour
        # if hour >= 24:
        #     hour -= 24
        timeStandard = "오전" if 0 <= hour  <12 else "오후"
        print(ele['created_at'])
        time += str(ele['created_at'].year) + "." + str(ele['created_at'].month).zfill(2) + "." + str(ele['created_at'].day).zfill(2) + " " \
                + timeStandard +" "+ str(hour).zfill(2) + ":" + str(ele['created_at'].minute).zfill(2) +":"+str(ele['created_at'].second).zfill(2)
        ele['time'] = time
        day =""
        day += str(ele['created_at'].year) + "." + str(ele['created_at'].month).zfill(2) + "." + str(ele['created_at'].day).zfill(2)
        ele['day'] = day
        
        # print(ele['time'], ele['day'])
        # temp += ele['created_at'].hour + ele['created_at'].hour +ele['created_at'].minute
        # print(ele['created_at'].hour)
        # print(ele['created_at'].minute)
        
        
    # print(commentList)
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


    return JsonResponse({'post_username':post_username,'post_user': post_user, 'post_id': post_id, 'post_title':post_title,  'post_content': post_content, 'post_created':post_created, 'photo_url':photo_url, 'ingredientL':ingredientL, 'comments': commentList, 'today':today, 'post_quantity': post_quantity})
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
    # print(Post.objects.all())
    post = get_object_or_404(Post, id=pk)
    comment_writer = request.POST.get('comment_writer')
    # print(comment_writer)
    # print(type(comment_writer))
    user_id = User.objects.all().get(username=comment_writer)
    
    # print(user_id, type(user_id))
    content = request.POST.get('content')
    if content:

        comment = Comment.objects.create(
            user_id = user_id,
            post_id = post,
            content = content,
        )
        post.save()

        data = {
            'comment_writer' : comment_writer,
            'writer_name' : user_id.name,
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
    print(Comment.objects.all())
    post = get_object_or_404(Post, id=pk)
    comment_id = request.POST.get('comment_id')

    target_comment = Comment.objects.get(pk = comment_id)
    print(target_comment)
    print(type(target_comment))
    if request.user == target_comment.user_id:

        target_comment.delete()
        # target_comment.deleted = True
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


