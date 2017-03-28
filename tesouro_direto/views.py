from rest_framework import viewsets
from tesouro_direto.models import CategoriaTitulo, OperacaoTitulo
from tesouro_direto.serializers import CategoriaTituloSerializer, OperacaoTituloSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from collections import OrderedDict
from datetime import datetime


class OperacaoTituloViewSet(viewsets.ModelViewSet):
    queryset = OperacaoTitulo.objects.all()
    serializer_class = OperacaoTituloSerializer

    def retrieve(self, request, pk=None):
        queryset = CategoriaTitulo.objects.all()
        categoria_titulo = get_object_or_404(queryset, pk=pk)
        operacao_titulo_list = OperacaoTitulo.objects.filter(categoria_titulo_id=categoria_titulo.id)

        additional_where = ''
        group_by = 'ano, mes'

        if request.query_params.get('data_inicio'):
            datetime_object = datetime.strptime(request.query_params.get('data_inicio'), '%d/%m/%Y')
            additional_where = " AND CAST(ano || substr('0' || mes, -2, 2) AS int) >= %s" % (datetime_object.strftime('%Y%m'))

        if request.query_params.get('data_fim'):
            datetime_object = datetime.strptime(request.query_params.get('data_fim'), '%d/%m/%Y')
            additional_where = " AND CAST(ano || substr('0' || mes, -2, 2) AS int) <= %s" % (datetime_object.strftime('%Y%m'))

        if request.query_params.get('group_by') == 'ano':
            group_by = 'ano'

        operacao_titulo_list = OperacaoTitulo.objects.raw(
            """
            SELECT
                id,
                mes,
                ano,
                SUM(CASE WHEN acao = 'venda' THEN valor END) AS valor_venda,
                SUM(CASE WHEN acao = 'resgate' THEN valor END) AS valor_resgate
            FROM tesouro_direto_operacaotitulo
            WHERE categoria_titulo_id = %d %s
            GROUP BY %s
            """ % (categoria_titulo.id, additional_where, group_by)
        )

        historico = [];

        for operacao_titulo in operacao_titulo_list:
            historico.append(
                OrderedDict([
                    ('mes', operacao_titulo.mes),
                    ('ano', operacao_titulo.ano),
                    ('valor_venda', operacao_titulo.valor_venda),
                    ('valor_resgate', operacao_titulo.valor_resgate),
                ])
            )

        return Response(
            OrderedDict([
                ('id', categoria_titulo.id),
                ('categoria_titulo', categoria_titulo.categoria_titulo),
                ('historico', historico),
            ])
        )
