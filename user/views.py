
import string
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def UserRegister(request):
    if request.method =='POST':
        kullanici = request.POST['kullanici']
        email = request.POST['email']
        sifre = request.POST['sifre']
        sifre2 = request.POST['sifre2']

        if kullanici !="" and email != "" and sifre !="":
            if sifre ==sifre2:
                #username'ın var olup olmadığını kontrol eder
                if User.objects.filter(username =kullanici).exists():
                    messages.error(request,'bu kullanıcı adı zaten mevcut')
                    return redirect("register")
                #email'i kontrol eder
                elif User.objects.filter(email=email).exists():
                    messages.error(request,"bu e-mail kullanımda")
                    return redirect("register")
                #şifre uzunluğunu kontrol eder
                elif len(sifre)<6:
                    messages.error(request,"şifre en az 6 karakter olması gerekiyor")
                    return redirect("register")
                #şifrede kullanıcı adı varmı?
                elif kullanici in sifre :
                    messages.error(request,"şifreniz ile kullanıcı adınız benzer olamaz")
                    return redirect("register")
                elif sifre[0] in string.ascii_lowercase:
                    messages.error(request,"baş harfi büyük olmalı")
                    return redirect("register")
                else:
                    # kullanıcıyı oluşturur
                    user =User.objects.create_user(username=kullanici ,email = email , password=sifre)
                    user.save()
                    messages.success(request,"kullanıcı oluşturuldu")
                    return redirect("index")
            else:
                messages.error(request,"şifreler uyuşmuyor")
                return redirect("register")
        else:
            messages.error(request,"tüm alanları doldurun")
            return redirect("register")
            
    return render(request,'register.html')

def userLogin(request):
    if request.method == "POST":
        kullanici = request.POST["kullanici"]
        sifre = request.POST["sifre"]

        user =authenticate(request,username=kullanici,password=sifre)
        if user is not None:
            login(request,user)
            messages.success(request,"giriş yapıldı")
            return redirect("index")
        else:
            messages.error(request,'kullanıcı adı veya şifre hatalı')
            return redirect("login")
    return render(request, 'login.html')
    
def userLogout(request):
    logout(request)
    messages.success(request,'çıkış yapıldı')
    return redirect('index')