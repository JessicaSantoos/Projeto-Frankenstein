from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50) 
    tipo = models.CharField(max_length=50) 
    data_aquisicao = models.DateField() 
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome
    
class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_reserva = models.DateTimeField(auto_now_add=True)
    data_desejada = models.DateField()

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome} - {self.quantidade}'

class Cadastro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome} - {self.quantidade}'