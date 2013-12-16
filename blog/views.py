from django.shortcuts import render,get_object_or_404
from blog.models import Blog,Post,Tag
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    context = {'blogs':Blog.objects.all(),'posts':Post.objects.all()[:10],'tags':Tag.objects.all()}
    return render(request,'blog/index.html',context)

def login_page(request):
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
    _user = get_object_or_404(User,username=username)
    if request.POST:
		_title = request.POST.get('title')
		if _title.strip() =='':
		    return render(request, 'blog/create_blog.html', {'user':_user,'error_message':"You have to write title for a blog."})
		b = Blog(user=_user,title=_title.strip())
		b.create_slug()
		b.save()
		return render(request,'blog/user_home.html',{'user':_user})
    else:
        return render(request, 'blog/create_blog.html', {'user':_user})
    
def sign_up(request):
    return HttpResponse("sign up a new user")
    
def post(request,slug):
    p = get_object_or_404(Post,slug=slug)
    blog = p.blog
    user = blog.user
    return render(request,'blog/post.html',{'post':p,'user':user})

def edit_post(request,slug):
    if request.user.is_authenticated():
        cur_user = request.user
        post = get_object_or_404(Post,slug=slug)
        blog = post.blog
        if cur_user != blog.user:
            return render(request,'blog/post.html',{
                'post':post,'error_message':"It's not your post, you can't edit"
                })
        else:
            #submited by user,return to post page
            if request.POST:
                _title = request.POST.get('title')
                if _title.strip() == '':
                    return render(request,'blog/edit_post.html',{
                        'post':post,
                        'error_message':"Title can't be blank",
                        })            
                _body = request.POST.get('body')
                post.title = _title
                post.body = _body
                post.save()
                return render(request, 'blog/post.html', {'post':post})
            else:
                # didn't submit
                return render(request,'blog/edit_post.html',{'post':post})            
    else:
        # anonymous users
        return render(request,'blog/post.html',{
                'post':post,'error_message':"You're not authenticated user, you can't edit"
                })

def create_post(request,slug):
    _blog = get_object_or_404(Blog,slug=slug)
    if request.POST:
        _title = request.POST.get('title')
        if _title.strip() == '':
            return render(request,'blog/create_post.html',{
                        'blog':_blog,
                        'error_message':"Title can't be blank",
                        })            
        _body = request.POST.get('body')
        _tags = request.POST.get('tags')
        post = Post(title=_title,body=_body,blog=_blog)
        post.create_slug()
        post.add_tags(_tags)
        post.save()
        return render(request, 'blog/post.html', {'post':post,'user':request.user})
    else:
        # didn't submit
        return render(request,'blog/create_post.html',{'blog':_blog})                    

def tag(request,slug):
    return HttpResponse("tag: %s" %slug)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
