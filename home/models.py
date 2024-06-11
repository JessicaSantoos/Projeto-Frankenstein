from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    quantidade = models.IntegerField(default=0)
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome
