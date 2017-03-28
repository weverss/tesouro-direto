from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tesouro_direto.models import CategoriaTitulo, OperacaoTitulo
from tesouro_direto.serializers import CategoriaTituloSerializer, OperacaoTituloSerializer
from collections import OrderedDict
from datetime import datetime


class OperacaoTituloViewSet(viewsets.ModelViewSet):
    queryset = OperacaoTitulo.objects.all()
    serializer_class = OperacaoTituloSerializer

    def retrieve(self, request, pk=None):
        """
        Lista de títulos com histórico de operações de venda e resgate
        """

        queryset = CategoriaTitulo.objects.all()
        categoria_titulo = get_object_or_404(queryset, pk=pk)
        start_date_where = self.get_start_date_where(request)
        end_date_where = self.get_end_date_where(request)
        group_by = self.get_group_by(request)

        operacao_titulo_list = OperacaoTitulo.objects.raw(
            """
            SELECT
                id,
                mes,
                ano,
                SUM(CASE WHEN acao = 'venda' THEN valor END) AS valor_venda,
                SUM(CASE WHEN acao = 'resgate' THEN valor END) AS valor_resgate
            FROM tesouro_direto_operacaotitulo
            WHERE categoria_titulo_id = %d %s %s
            GROUP BY %s
            """ % (categoria_titulo.id, start_date_where, end_date_where, group_by)
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

    @list_route()
    def comparar(self, request):
        """
        Comparação de valores de venda e resgate de títulos
        """

        if not request.query_params.get('ids'):
            return Response('Parâmetro "ids" obrigatório e não informado!', 400)

        ids = request.query_params.get('ids')
        start_date_where = self.get_start_date_where(request)
        end_date_where = self.get_end_date_where(request)
        group_by = self.get_group_by(request)

        titulo_list = CategoriaTitulo.objects.raw(
            """
            SELECT
                c.id,
                c.categoria_titulo,
                o.mes,
                o.ano,
                SUM(CASE WHEN o.acao = 'venda' THEN o.valor END) AS valor_venda,
                SUM(CASE WHEN o.acao = 'resgate' THEN o.valor END) AS valor_resgate
             FROM tesouro_direto_operacaotitulo o
             INNER JOIN tesouro_direto_categoriatitulo c ON c.id = o.categoria_titulo_id
             WHERE c.id IN (%s) %s %s
             GROUP BY c.id
            """ % (ids, start_date_where, end_date_where)
        )

        valores = [];

        for titulo in titulo_list:
            valores.append(
                OrderedDict([
                    ('id', titulo.id),
                    ('categoria_titulo', titulo.categoria_titulo),
                    ('valor_venda', titulo.valor_venda),
                    ('valor_resgate', titulo.valor_resgate),
                ])
            )

        return Response(
            OrderedDict([
                ('ano', titulo_list[0].ano),
                ('mes', titulo_list[0].mes),
                ('categoria_titulo', titulo_list[0].categoria_titulo),
                ('valores', valores),
            ])
        )

    @list_route(url_path='(venda|resgate)/(\d+)')
    def venda(self, request, acao, pk):
        """
        Lista valores de venda/resgate de um determinado título
        """

        start_date_where = self.get_start_date_where(request)
        end_date_where = self.get_end_date_where(request)
        group_by = 'id'

        if request.query_params.get('group_by'):
            group_by = request.query_params.get('group_by')

        operacao_titulo_list = OperacaoTitulo.objects.raw(
            """
            SELECT *, SUM(valor) AS valor
            FROM tesouro_direto_operacaotitulo o
            WHERE categoria_titulo_id = %s AND acao = '%s' %s %s
            GROUP BY %s
            """ % (pk, acao, start_date_where, end_date_where, group_by)
        )

        data = [];

        for operacao_titulo in operacao_titulo_list:
            data.append(
                OrderedDict([
                    ('id', operacao_titulo.id),
                    ('categoria_titulo', operacao_titulo.categoria_titulo.categoria_titulo),
                    ('mes', operacao_titulo.mes),
                    ('ano', operacao_titulo.ano),
                    ('acao', operacao_titulo.acao),
                    ('valor', operacao_titulo.valor),
                ])
            )

        return Response(data)

    def get_start_date_where(self, request):
        """
        Retorna parâmetro data de inicio em formato SQL.
        """

        if request.query_params.get('data_inicio'):
            datetime_object = datetime.strptime(request.query_params.get('data_inicio'), '%d/%m/%Y')
            return " AND CAST(ano || substr('0' || mes, -2, 2) AS int) >= %s" % (datetime_object.strftime('%Y%m'))
        return ''

    def get_end_date_where(self, request):
        """
        Retorna parâmetro data de fim em formato SQL.
        """

        if request.query_params.get('data_fim'):
            datetime_object = datetime.strptime(request.query_params.get('data_fim'), '%d/%m/%Y')
            return " AND CAST(ano || substr('0' || mes, -2, 2) AS int) >= %s" % (datetime_object.strftime('%Y%m'))
        return ''

    def get_group_by(self, request):
        """
        Retorna parâmetro group_by em formato SQL.
        """

        if request.query_params.get('group_by'):
            return request.query_params.get('group_by')
        return 'ano, mes'
