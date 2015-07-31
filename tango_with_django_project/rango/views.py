#coding=utf-8
from django.shortcuts import render
from rango.models import Page,Category
from forms import *
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
def  rango(request):
	str = " hi,<a href='/rango/about/'>前往about页面</a>"
		  
	return HttpResponse(str) 
def about(request):
	str = "Rango says here is the about page <a href='/rango/'>回到主页</a> "
	return HttpResponse(str) 
def index(request):

    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = int(request.COOKIES.get('visits', '1'))#
    reset_last_visit_time = False
    response = render(request, 'index.html', context_dict)
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S") # 最后7位是GMT，格林尼治时间不用去管

        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        context_dict['visits'] = visits
        response = render(request, 'index.html', context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)

    return response
 
def category(request, category_name_slug):

    context_dict = {}

    try:

        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category.slug
    except Category.DoesNotExist:
              pass
    return render(request, 'category.html', context_dict)
from rango.forms import CategoryForm

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
                print form.errors
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def add_page(request, category_name_slug):
        try:
                cat = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
                cat = None
        if request.method == 'POST':
                form = PageForm(request.POST)
                if form.is_valid():
                        if cat:
                                page = form.save(commit=False)#根据表单返回一个page类的对象，不保存到数据库，之后再保存就用commit=False
                                page.category = cat
                                page.views = 0
                                page.save()
                                return category(request, category_name_slug)
                else:
                        print(form.errors)
        else:
                form = PageForm()
        context_dict = {'form':form, 'category_name_slug': cat.slug}
        return render(request, 'add_page.html', context_dict)

def register(request):
        registered = False
        if request.method=='POST':
                userForm = UserForm(data=request.POST)
                profileForm = UserProfileForm(data=request.POST)
                if userForm.is_valid() and profileForm.is_valid():
                        user = userForm.save()
                        user.set_password(user.password)#use hash encrypt
                        user.save()
                        profile = profileForm.save(commit = False)
                        profile.user  = user
                        if 'picture' in request.FILES:
                                profile.save()
                        registered = True 
                else:
                        print userForm.errors, profileForm.errors
        else:
                userForm = UserForm()
                profileForm = UserProfileForm()
        dict = {'user_form': userForm, 'profile_form': profileForm, 'registered': registered} 
        return render(request,'register.html',dict)

def user_login(request):
    # If the request is a HTTP POST, try to pull out拿出 the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'login.html', ) #没有要替换的内容，第三个参数默认是空字典

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
