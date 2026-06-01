# Generated manually on 2026-05-31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0003_configbolao_lock_publico'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='precisa_redefinir_pin',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ResultadoClassificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicao', models.PositiveSmallIntegerField()),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultado_classificacao', to='bolao.grupo')),
                ('selecao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bolao.selecao')),
            ],
            options={
                'ordering': ['grupo', 'posicao'],
                'unique_together': {('grupo', 'posicao')},
            },
        ),
        migrations.CreateModel(
            name='ResultadoExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('campeao', 'Campeão'), ('vice', 'Vice-Campeão'), ('terceiro', 'Terceiro Colocado'), ('pior', 'Pior Seleção')], max_length=10, unique=True)),
                ('selecao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bolao.selecao')),
            ],
        ),
    ]
