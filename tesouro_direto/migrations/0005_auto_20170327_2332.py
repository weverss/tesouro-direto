# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 23:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tesouro_direto', '0004_auto_20170327_2224'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TituloTesouro',
            new_name='CategoriaTitulo',
        ),
        migrations.RenameField(
            model_name='operacaotitulo',
            old_name='titulo_tesouro',
            new_name='categoria_titulo',
        ),
    ]
