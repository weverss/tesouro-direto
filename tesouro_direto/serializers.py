from rest_framework import serializers
from tesouro_direto.models import CategoriaTitulo, OperacaoTitulo


class OperacaoTituloSerializer(serializers.ModelSerializer):
    categoria_titulo = serializers.StringRelatedField()

    class Meta:
        model = OperacaoTitulo
        fields = ('id', 'categoria_titulo', 'mes', 'ano', 'acao', 'valor')

    def create(self, validated_data):
        request = self.context.get("request")
        categoria_titulo = request.data.get('categoria_titulo')
        categoria_titulo_instance = CategoriaTitulo.objects.filter(categoria_titulo=categoria_titulo).first()

        operacao_titulo = OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo_instance, **validated_data)
        return operacao_titulo

    def update(self, instance, validated_data):
        request = self.context.get("request")

        categoria_titulo = request.data.get('categoria_titulo')
        instance.categoria_titulo = CategoriaTitulo.objects.filter(categoria_titulo=categoria_titulo).first()

        instance.mes = validated_data.get('mes', instance.mes)
        instance.ano = validated_data.get('ano', instance.ano)
        instance.acao = validated_data.get('acao', instance.acao)
        instance.valor = validated_data.get('valor', instance.valor)

        instance.save()
        return instance

class CategoriaTituloSerializer(serializers.ModelSerializer):
    historico = OperacaoTituloSerializer(many=True, read_only=True)

    class Meta:
        model = CategoriaTitulo
        fields = ('id', 'categoria_titulo', 'historico')
