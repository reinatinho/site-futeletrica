# Generated manually on 2026-05-21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0002_jogo_descricao_jogo_numero_jogo_alter_jogo_fase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configbolao',
            name='lock_fase_grupos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_16avos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_oitavas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_quartas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_semi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_terceiro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='lock_final',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_fase_grupos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_16avos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_oitavas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_quartas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_semi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_terceiro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configbolao',
            name='publico_final',
            field=models.BooleanField(default=False),
        ),
    ]
