from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get("senha")

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/home/estoque')

        messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
        return redirect('/users/login')
    
def sair(request):
    auth.logout(request)
    return redirect('/users/login')