from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('estoque/', views.estoque_view, name="estoque"),
    path('cadastrar/', views.cadastrar_view, name="cadastrar"),
    path('remover/', views.remover_view, name="remover"),
    path('entre_em_contato/', views.entre_em_contato_view, name='entre_em_contato'),
]
