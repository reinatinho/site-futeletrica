from django.contrib import admin
from .models import (
    Participante, Grupo, Selecao, Jogo,
    Palpite, PalpiteClassificacao, PalpiteExtra, ConfigBolao
)


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome', 'sobrenome', 'criado_em']
    search_fields = ['username', 'nome', 'sobrenome']


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['letra', 'nome']


@admin.register(Selecao)
class SelecaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'bandeira_emoji', 'grupo']
    list_filter = ['grupo']


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['selecao_casa', 'selecao_fora', 'data_hora', 'grupo', 'gols_casa', 'gols_fora']
    list_filter = ['grupo', 'fase']


@admin.register(Palpite)
class PalpiteAdmin(admin.ModelAdmin):
    list_display = ['participante', 'jogo', 'gols_casa', 'gols_fora', 'pontos']
    list_filter = ['participante', 'jogo__grupo']


@admin.register(PalpiteClassificacao)
class PalpiteClassificacaoAdmin(admin.ModelAdmin):
    list_display = ['participante', 'grupo', 'posicao', 'selecao']
    list_filter = ['grupo']


@admin.register(PalpiteExtra)
class PalpiteExtraAdmin(admin.ModelAdmin):
    list_display = ['participante', 'tipo', 'selecao']
    list_filter = ['tipo']


@admin.register(ConfigBolao)
class ConfigBolaoAdmin(admin.ModelAdmin):
    list_display = ['fase_grupos_aberta', 'fase_16avos_aberta', 'palpites_publicos']
