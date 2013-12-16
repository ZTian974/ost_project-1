from django.shortcuts import render,get_object_or_404
from blog.models import Blog,Post,Tag
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    context = {'blogs':Blog.objects.all(),'posts':Post.objects.all()[:10],'tags':Tag.objects.all()}
    return render(request,'blog/index.html',context)

def login_page(request):
    return render(request,'blog/login.html',{'error_message':''})


def login_check(request):
    if request.POST:
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        user = authenticate(username = _username, password = _password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request,'blog/user_home.html',{'user':user})
        else:
            return render(request,'blog/login.html',{'error_message':"ERROR: password and username didn't match!"})
    else:
            return render(request,'blog/login.html',{'error_message':''})
            
def blog_posts(request,slug):
    blog = get_object_or_404(Blog,slug=slug)
    posts = blog.post_set.all()
    return render(request,'blog/blog_posts.html',{
        'blog':blog,
        'posts':posts,    
    })

def create_blog(request,username):
    user = get_object_or_404(User,username=username)
    return render(request, 'blog/create_blog.html', {'user':user})
