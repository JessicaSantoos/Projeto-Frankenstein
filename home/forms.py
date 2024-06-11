from django import forms
from .models import Produto
from .models import Reserva

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'quantidade']

class RemoverProdutoForm(forms.Form):
    quantidade = forms.IntegerField(min_value=1, label='Quantidade a ser removida')

    def __init__(self, *args, **kwargs):
        super(RemoverProdutoForm, self).__init__(*args, **kwargs)
        produtos = Produto.objects.all()
        choices = [(produto.id, produto.nome) for produto in produtos]
        self.fields['produto'] = forms.ChoiceField(choices=choices, label='Produto', widget=forms.Select(attrs={'class': 'form-control'}))
        

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['produto', 'quantidade', 'data_desejada']
        widgets = {
            'data_desejada': forms.DateInput(attrs={'type': 'date'}),
        }