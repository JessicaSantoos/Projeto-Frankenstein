from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto
from django.core.mail import send_mail
from django.contrib import messages
import openai
from django.conf import settings
from .forms import ProdutoForm
from .forms import RemoverProdutoForm

openai.api_key = settings.OPENAI_API_KEY

# |Tela HOME (NavBar)
@login_required
def home_view(request):
    return render(request, 'home/navbar.html')

# |Tela Estoque de Produtos
@login_required
def estoque_view(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque.html', {'produtos': produtos})

# |Tela Cadastro de Produtos
@login_required
def cadastrar_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            quantidade = form.cleaned_data['quantidade']
            
            # Verifica se o produto já existe no estoque
            produto_existente = Produto.objects.filter(nome=nome).first()
            if produto_existente:
                produto_existente.quantidade += quantidade
                produto_existente.save()
                messages.success(request, f'{quantidade} unidades de {nome} adicionadas ao estoque.')
            else:
                form.save()
                messages.success(request, 'Produto cadastrado com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os dados e tente novamente.')
    else:
        form = ProdutoForm()
    
    return render(request, 'cadastrar.html', {'form': form})

# |Tela Remover Produtos
@login_required
def remover_view(request):
    produtos = Produto.objects.all()

    if request.method == 'POST':
        form = RemoverProdutoForm(request.POST)
        if form.is_valid():
            produto_id = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']

            produto = Produto.objects.get(pk=produto_id)

            # Verifica se a quantidade a ser removida é menor ou igual à quantidade disponível no estoque
            if quantidade <= produto.quantidade:
                produto.quantidade -= quantidade
                produto.save()

                # Se a quantidade do produto for zero após a remoção, exclua o produto do banco de dados
                if produto.quantidade == 0:
                    produto.delete()
                    messages.success(request, f'{quantidade} unidades de {produto.nome} removidas do estoque. O produto foi completamente removido.')
                else:
                    messages.success(request, f'{quantidade} unidades de {produto.nome} removidas do estoque.')
                return redirect('remover')
            else:
                messages.error(request, f'A quantidade a ser removida é maior do que a quantidade disponível ({produto.quantidade}).')
    else:
        form = RemoverProdutoForm()

    return render(request, 'remover.html', {'produtos': produtos, 'form': form})

# |Tela Suporte
@login_required
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

        except openai.error.RateLimitError:
            bot_response = "Você excedeu seu limite de uso da API. Por favor, tente novamente mais tarde ou verifique seu plano e detalhes de faturamento."
        except openai.error.OpenAIError as e:
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


