from django.shortcuts import render,get_object_or_404,render_to_response
from blog.models import Blog,Post,Tag, DocumentForm, Document
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import re,copy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.core.urlresolvers import reverse

def index(request):
    context = {
        'blogs':Blog.objects.all(),
        'posts':Post.objects.all()[:10],
        'tags':Tag.objects.all()
        }
    return render(request,'blog/index.html',context)

def logout_page(request):
    logout(request)
    context = {
        'blogs':Blog.objects.all(),
        'posts':Post.objects.all()[:10],
        'tags':Tag.objects.all()
        }
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
            return render(request,'blog/login.html',{
                'error_message':"ERROR: password and username didn't match!"
                })
    else:
            return render(request,'blog/login.html',{'error_message':''})

def short_body(posts):
    posts_500c=copy.deepcopy(posts)
    for post in posts_500c:
        if len(post.body) > 500:
            post.body = post.body[:500] + "......Please click the title of post to read origianl contents"
    return posts_500c
            
def blog_posts(request,slug):
    blog = get_object_or_404(Blog,slug=slug)
    user = blog.user
    posts = blog.post_set.all()
    paginator = Paginator(posts,10)
    page = request.GET.get('page')
    try:
        post_page = paginator.page(page)
    except PageNotAnInteger:
        post_page = paginator.page(1)
    except EmptyPage:
        post_page = paginator.page(paginator.num_pages)
    return render(request,'blog/blog_posts.html',{'blog':blog,'posts':post_page,'user':user,})

def create_blog(request,username):
    _user = get_object_or_404(User,username=username)
    if not request.user.is_authenticated():
        return render(request,'blog/user_home.html',{
            'user':_user,
            'error_message':"it's not your space, you can't create a blog",
            })
    if request.POST:
		_title = request.POST.get('title')
		if _title.strip() =='':
		    return render(request, 'blog/create_blog.html', {
		        'user':_user,
		        'error_message':"You have to write title for a blog."
		        })
		b = Blog(user=_user,title=_title.strip())
		b.create_slug()
		b.save()
		return render(request,'blog/user_home.html',{'user':_user})
    else:
        return render(request, 'blog/create_blog.html', {'user':_user})

def valid_username(s):
    p = re.compile(r'^[\d\w_]+$')
    if p.match(s.strip()) == None:
        return False
    else:
        return True
    
def sign_up(request):
    if request.POST:
        _username = request.POST.get('username')
        if valid_username(_username) == False:
            return render(request,'blog/sign_up.html',{
                'error_message':"username can only have digital, letter and '_'."
                })
        if User.objects.filter(username = _username.strip()) :
            return render(request,'blog/sign_up.html',{
                'error_message':("the username: '%s' has been registered." %_username)
                })
        _pw = request.POST.get('password')
        _pw2 = request.POST.get('password_re')
        if _pw != _pw2:
            return render(request,'blog/sign_up.html',{
                'error_message':"Two passwords didn't match,please confirm they are the same."
                })
        _user = User.objects.create_user(_username.strip(),'',_pw)
        user = authenticate(username = _username, password = _pw)
        if user is not None and user.is_active:
            login(request, user)
            return render(request,'blog/user_home.html',{'user':user})
        else:
            return render(request,'blog/sign_up.html',{
                'error_message':"ERROR: sign up failed."
                })
    else:
        return render(request, 'blog/sign_up.html',{})
    
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
                'post':post,
                'error_message':"It's not your post, you can't edit",
                'user':blog.user,
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
                _tags = request.POST.get('tags')
                post.title = _title
                post.body = _body
                post.add_tags(_tags)
                post.save()
                return render(request, 'blog/post.html', {'post':post})
            else:
                # didn't submit
                return render(request,'blog/edit_post.html',{'post':post})            
    else:
        # anonymous users
        post = get_object_or_404(Post,slug=slug)
        user = post.blog.user
        return render(request,'blog/post.html',{
                'post':post,
                'user':user,
                'error_message':"You're not authenticated user, you can't edit",
                })

def create_post(request,slug):
    _blog = get_object_or_404(Blog,slug=slug)
    blog_user = _blog.user
    posts = _blog.post_set.all()
    if blog_user != request.user:
        return render(request,'blog/blog_posts.html',{
            'blog':_blog,
            'posts':posts,
            'user':blog_user,
            'error_message':"It's not your blog, you can't create a post here.",                
        })        
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
    tag = get_object_or_404(Tag,slug=slug)
    posts = tag.post_set.all()
    paginator = Paginator(posts,10)
    page = request.GET.get('page')
    try:
        post_page = paginator.page(page)
    except PageNotAnInteger:
        post_page = paginator.page(1)
    except EmptyPage:
        post_page = paginator.page(paginator.num_pages)
    return render(request, 'blog/tag.html',{
        'tag':tag,
        'posts':post_page,
        })
    
def lists(request):        
        # Handle file upload
    if request.user.is_authenticated() == False:
        error_message="You're not authenticated user, you can't upload_file"
        return render_to_response('blog/upload_file.html',
            {'documents': Document.objects.all(),
             'form': DocumentForm(),
             'error_message':error_message},
            context_instance=RequestContext(request)
        )
    else:
        error_message=''        
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('blog:upload_file'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response('blog/upload_file.html',
        {'documents': documents, 'form': form, 'error_message':error_message},
        context_instance=RequestContext(request)
    )    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
