from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto, Reserva
from .forms import ReservaForm
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

# |Tela Estoque de Produtos Reservados
@login_required
def reservas_view(request):
    produto_id = request.GET.get('produto')
    if produto_id:
        reservas = Reserva.objects.filter(produto_id=produto_id)
    else:
        reservas = Reserva.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'reservas.html', {'reservas': reservas, 'produtos': produtos})

# |Tela Cadastro de Produtos
@login_required
def cadastrar_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            quantidade = form.cleaned_data['quantidade']
            
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

            if quantidade <= produto.quantidade:
                produto.quantidade -= quantidade
                produto.save()

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

# | Tela Reservar Produto
@login_required
def reservar_view(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            produto = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']
            data_desejada = form.cleaned_data['data_desejada']

            if quantidade <= produto.quantidade:
                produto.quantidade -= quantidade
                produto.save()
                
                Reserva.objects.create(
                    usuario=request.user,
                    produto=produto,
                    quantidade=quantidade,
                    data_desejada=data_desejada
                )
                
                messages.success(request, f'Reserva de {quantidade} unidades de {produto.nome} para {data_desejada} realizada com sucesso!')
                return redirect('reservar')
            else:
                messages.error(request, f'A quantidade desejada é maior do que a quantidade disponível ({produto.quantidade}).')
    else:
        form = ReservaForm()

    return render(request, 'reservar.html', {'form': form})

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


