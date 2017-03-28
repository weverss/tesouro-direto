from django.db import models


class CategoriaTitulo(models.Model):
    CATEGORIAS = (
        ('LTN', 'LTN'),
        ('LFT', 'LFT'),
        ('NTN-B', 'NTN-B'),
        ('NTN-B Principal', 'NTN-B Principal'),
        ('NTN-C', 'NTN-C'),
        ('NTN-F', 'NTN-F'),
    )

    categoria_titulo = models.CharField(choices=CATEGORIAS, max_length=15)

    def __str__(self):
        return self.categoria_titulo

class OperacaoTitulo(models.Model):
    ACOES = (
        ('venda', 'venda'),
        ('resgate', 'resgate'),
    )

    categoria_titulo = models.ForeignKey(CategoriaTitulo, on_delete=models.CASCADE)
    mes = models.IntegerField()
    ano = models.IntegerField()
    acao = models.CharField(choices=ACOES, max_length=7)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
