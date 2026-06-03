# Generated manually on 2026-06-03

from datetime import datetime
from django.db import migrations
from django.utils import timezone


RENOMEAR = {
    'BIH': 'Bósnia',
    'COD': 'Congo',
    'KOR': 'Coreia do Sul',
    'CIV': 'C. do Marfim',
    'USA': 'EUA',
    'CZE': 'Rep. Tcheca',
}

# (codigo_casa, codigo_fora, nova data/hora)
CORRIGIR_DATAS = [
    ('TUR', 'PAR', '2026-06-20 01:00'),
    ('TUN', 'JPN', '2026-06-21 01:00'),
    ('JOR', 'ARG', '2026-06-27 23:00'),
    ('UZB', 'COL', '2026-06-17 23:00'),
]


def aplicar(apps, schema_editor):
    Selecao = apps.get_model('bolao', 'Selecao')
    Jogo = apps.get_model('bolao', 'Jogo')

    for codigo, novo_nome in RENOMEAR.items():
        Selecao.objects.filter(codigo=codigo).update(nome=novo_nome)

    for cod_casa, cod_fora, data_str in CORRIGIR_DATAS:
        dt = timezone.make_aware(datetime.strptime(data_str, '%Y-%m-%d %H:%M'))
        Jogo.objects.filter(
            fase='grupos',
            selecao_casa__codigo=cod_casa,
            selecao_fora__codigo=cod_fora,
        ).update(data_hora=dt)


def reverter(apps, schema_editor):
    # Sem reversão automática (mantém os novos valores)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0004_pin_resultados_oficiais'),
    ]

    operations = [
        migrations.RunPython(aplicar, reverter),
    ]
