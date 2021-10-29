from django import forms
from django.shortcuts import render
from Login_app import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def login_page(request):
    return render(request,'Login_app/login.html', context={})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("Account is not active!")
        else:

            return HttpResponse('Login details are wrong!')

    else:
        return render(request,'Login_app/login.html', context={})
                    

def index(request):
    diction = {}
    return render(request, 'Login_app/index.html', context=diction)
def register(request):
    registered = False
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        user_info_form = forms.UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            user_info.save()
            registered = True    

    else:
        user_form = forms.UserForm()
        user_info_form = forms.UserInfoForm()
    diction = {'user_form': user_form, 'user_info_form':user_info_form, 'registered': registered}
    return render(request,'Login_app/register.html', context=diction)    