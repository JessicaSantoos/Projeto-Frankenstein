from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'tipo', 'data_aquisicao', 'quantidade']  # Exibe esses campos na lista de produtos no Django Admin
    search_fields = ['nome']  # Permite pesquisar produtos pelo nome
