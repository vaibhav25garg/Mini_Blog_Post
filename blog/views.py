from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

#Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

#About
def about(request):
    response = render(request, 'blog/about.html')
    response.set_cookie('vaibhav','garg')
    return response

#Contact
def contact(request):
    nm = request.COOKIES['vaibhav']
    return render(request, 'blog/contact.html',{'name':nm})

#Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        # ip = request.session.get("ip", 0) #for finding ip of any user
        return render(request, 'blog/dashboard.html',{'posts':posts, 'full_name': full_name, 'groups':gps},)
    else:
        return HttpResponseRedirect('/login/')

#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

#Signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            return HttpResponseRedirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form':form})

#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                messages.success(request, 'Post Added Successfully')
                pst.save()
                form = PostForm()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#Update/Edit Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                messages.success(request, 'Post Updated Successfully')
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

#Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            messages.success(request, 'Post deleted Successfully')
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
