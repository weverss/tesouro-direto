import zipfile
import datetime
from xml.etree.ElementTree import iterparse
from django.core.management.base import BaseCommand, CommandError
from tesouro_direto.models import CategoriaTitulo, OperacaoTitulo

class Command(BaseCommand):
    help = 'Importa planilha de séries temporais do Tesouro Direto'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        filepath = options['filepath']
        zfile = zipfile.ZipFile(filepath)

        for e, el in iterparse(zfile.open('xl/worksheets/sheet1.xml')):
            if el.tag.endswith('row') and int(el.attrib.get('r')) >= 12:
                self.import_row(el)

        self.stdout.write(self.style.SUCCESS('Importação do arquivo "%s" finalizada.' % filepath))

    def import_row(self, element):
        self.stdout.write('Importando linha %s' % element.attrib.get('r'))

        mes = self.get_month(element[1][0].text)
        ano = self.get_year(element[1][0].text)

        for child in element:
            valor = float(child[0].text) * 1000000

            if (child.attrib.get('r').startswith('C')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='LTN')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('D')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='LFT')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('E')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-B')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('F')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-B Principal')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('G')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-C')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('H')):
                acao = 'venda'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-F')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('I')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='LTN')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('J')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='LFT')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('K')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-B')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('L')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-B Principal')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('M')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-C')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

            elif (child.attrib.get('r').startswith('N')):
                acao = 'resgate'
                categoria_titulo, created = CategoriaTitulo.objects.get_or_create(categoria_titulo='NTN-F')
                OperacaoTitulo.objects.create(categoria_titulo=categoria_titulo, mes=mes, ano=ano, acao=acao, valor=valor)

    def get_month(self, serial_date):
        return self.get_date(serial_date).strftime('%m')

    def get_year(self, serial_date):
        return self.get_date(serial_date).strftime('%Y')

    def get_date(self, serial_date):
        return datetime.datetime(1900, 1, 1, 0, 0) + datetime.timedelta(int(serial_date) - 1)
