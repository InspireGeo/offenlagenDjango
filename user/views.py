from typing import NewType
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME, login,authenticate,logout
# Create your views here.

def register(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()

        login(request,newUser)
        messages.success(request, 'Başarı ile Kayıt OLdunuz')
        return redirect("index")
    context = {
            "form" : form
        }
    return render(request,"register.html",context)




    """ ders 214
    if  request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()

            login(request,newUser)
            return redirect("index")
        context = {
            "form" : form
        }
        return render(request,"register.html",context)

    else:


        form = RegisterForm()
        context = {
            "form" : form
        }
        return render(request,"register.html",context)

"""




    """ ders-213
    form = RegisterForm()
    context = {
        "form" : form
    }


    return render(request, "register.html",context)"""


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username =username,password = password)
        if user is None:
            messages.warning(request,"Kullanıcı Adı veya Parola HAtlı")
            return render(request, "login.html", context)
        messages.success(request,"Başarılı giriş  Yaptınız")                    
        login(request,user)
        return redirect("index")
    return render (request,"login.html",context)
    



    return render(request, "login.html")
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("index")
