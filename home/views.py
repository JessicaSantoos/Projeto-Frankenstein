from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Produto
from django.core.mail import send_mail
from django.contrib import messages
import openai
from django.conf import settings
from openai.error import RateLimitError, OpenAIError
import socket

# Configure a API key do OpenAI
openai.api_key = settings.OPENAI_API_KEY

# |Tela HOME (NavBar)
@login_required
def home_view(request):
    return render(request, 'home/navbar.html')

# |Tela Estoque de Prosdutos
@ensure_csrf_cookie
@login_required
def estoque_view(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque.html', {'produtos': produtos})

# |Tela Cadastro de Produtos
@login_required
def cadastrar_view(request):
    return render(request, 'cadastrar.html')

# |Tela Remover Produtos
@login_required
def remover_view(request):
    return render(request, 'remover.html')

# |Tela Suporte
@login_required
@ensure_csrf_cookie
def entre_em_contato_view(request):
    bot_response = ""
    user_input = ""

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        user_email = request.POST.get('user_email')

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            bot_response = response.choices[0].message['content'].strip()

        except RateLimitError:
            bot_response = "Você excedeu seu limite de uso da API. Por favor, tente novamente mais tarde ou verifique seu plano e detalhes de faturamento."
        except OpenAIError as e:
            bot_response = f"Erro ao acessar a API do OpenAI: {e}"
        except Exception as e:
            bot_response = f"Ocorreu um erro inesperado: {e}"

        if 'send_to_support' in request.POST:
            message = request.POST.get('message')
            try:
                send_mail(
                    'Dúvida de Usuário',
                    f'Dúvida de {user_email}: {message}',
                    settings.EMAIL_HOST_USER,
                    ['extreme.revolution18@gmail.com'],  # E-mail do suporte
                    fail_silently=False,
                )
                messages.success(request, 'Dúvida enviada para o suporte!')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {e}")
            return redirect('entre_em_contato')

    return render(request, 'entre_em_contato.html', {
        'user_input': user_input,
        'bot_response': bot_response,
    })

# |Funções do Bot
@login_required
def send_email_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        send_to_support = request.POST.get('send_to_support')
        user_email = request.POST.get('user_email')
        
        if send_to_support:
            try:
                send_mail(
                    'Dúvida de Usuário',
                    f'Dúvida de {user_email}: {message}',
                    settings.EMAIL_HOST_USER,
                    ['extreme.revolution18@gmail.com'],  # E-mail do suporte
                    fail_silently=False,
                )
                messages.success(request, 'Dúvida enviada para o suporte!')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {e}")
            return redirect('entre_em_contato')
        else:
            messages.success(request, 'Obrigado por entrar em contato!')
            return redirect('entre_em_contato')
    else:
        return redirect('entre_em_contato')

@login_required
def solicitar_duvida_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user_email = request.POST.get('user_email')
        message = request.POST.get('message')
        try:
            send_mail(
                'Dúvida de Usuário',
                f'Nome: {name}\nEmail: {user_email}\n\n{message}',
                settings.EMAIL_HOST_USER,
                ['extreme.revolution18@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Dúvida enviada com sucesso!')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {e}")
        return redirect('entre_em_contato')
    return render(request, 'solicitar_duvida.html')

def get_site_info():
    with open('site_info.txt', 'r') as file:
        return file.read()