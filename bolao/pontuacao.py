from .models import (
    Participante, Palpite, PalpiteClassificacao, PalpiteExtra,
    Jogo, Grupo, Selecao, ResultadoClassificacao, ResultadoExtra,
)

# Fases eliminatórias valem o dobro de pontos (a partir dos 16-avos)
FASES_ELIMINATORIAS = {'16avos', 'oitavas', 'quartas', 'semi', 'terceiro', 'final'}

# Pontuação dos palpites especiais (campeão, vice, 3º, pior)
PONTOS_EXTRA = 20


def calcular_pontos_jogo(palpite_casa, palpite_fora, resultado_casa, resultado_fora, multiplicador=1):
    """
    Calcula pontos de um palpite individual.
    Retorna: 10 (perfeito), 8 (quase perfeito), 5 (resultado), 3 (simples), 0 (errou).
    O multiplicador dobra a pontuação nas fases eliminatórias.
    """
    if palpite_casa is None or palpite_fora is None:
        return 0
    if resultado_casa is None or resultado_fora is None:
        return None

    if palpite_casa == resultado_casa and palpite_fora == resultado_fora:
        return 10 * multiplicador

    palpite_vencedor = 'casa' if palpite_casa > palpite_fora else ('fora' if palpite_fora > palpite_casa else 'empate')
    resultado_vencedor = 'casa' if resultado_casa > resultado_fora else ('fora' if resultado_fora > resultado_casa else 'empate')

    acertou_vencedor = (palpite_vencedor == resultado_vencedor)
    acertou_gols_casa = (palpite_casa == resultado_casa)
    acertou_gols_fora = (palpite_fora == resultado_fora)

    if acertou_vencedor and (acertou_gols_casa or acertou_gols_fora):
        return 8 * multiplicador

    if acertou_vencedor:
        return 5 * multiplicador

    if acertou_gols_casa or acertou_gols_fora:
        return 3 * multiplicador

    return 0


def multiplicador_fase(fase):
    """Retorna o multiplicador de pontos para a fase do jogo."""
    return 2 if fase in FASES_ELIMINATORIAS else 1


def calcular_classificacao_real_grupo(grupo):
    """
    Calcula a classificação real de um grupo com base nos resultados oficiais.
    Retorna lista ordenada de dicts: [{selecao_id, pts, sg, gp, ...}, ...]
    """
    selecoes = list(grupo.selecoes.values_list('id', flat=True))
    stats = {s: {'id': s, 'pts': 0, 'v': 0, 'e': 0, 'd': 0, 'gp': 0, 'gc': 0, 'sg': 0} for s in selecoes}

    jogos = grupo.jogos.filter(fase='grupos', gols_casa__isnull=False, gols_fora__isnull=False)
    for jogo in jogos:
        casa_id = jogo.selecao_casa_id
        fora_id = jogo.selecao_fora_id
        gc = jogo.gols_casa
        gf = jogo.gols_fora

        stats[casa_id]['gp'] += gc
        stats[casa_id]['gc'] += gf
        stats[fora_id]['gp'] += gf
        stats[fora_id]['gc'] += gc

        if gc > gf:
            stats[casa_id]['v'] += 1
            stats[casa_id]['pts'] += 3
            stats[fora_id]['d'] += 1
        elif gc < gf:
            stats[fora_id]['v'] += 1
            stats[fora_id]['pts'] += 3
            stats[casa_id]['d'] += 1
        else:
            stats[casa_id]['e'] += 1
            stats[casa_id]['pts'] += 1
            stats[fora_id]['e'] += 1
            stats[fora_id]['pts'] += 1

    for s in stats.values():
        s['sg'] = s['gp'] - s['gc']

    sorted_stats = sorted(stats.values(), key=lambda x: (-x['pts'], -x['sg'], -x['gp']))
    return sorted_stats


def calcular_pontos_classificacao(participante, grupo, real_dict):
    """
    Calcula pontos pela classificação do grupo.
    1º=8pts, 2º=6pts, 3º=4pts, 4º=2pts
    real_dict: dict {posicao: selecao_id} com o resultado oficial.
    """
    pontos_por_posicao = {1: 8, 2: 6, 3: 4, 4: 2}
    total = 0

    palpites = PalpiteClassificacao.objects.filter(
        participante=participante, grupo=grupo
    ).values_list('posicao', 'selecao_id')

    palpite_dict = {pos: sel_id for pos, sel_id in palpites}

    for pos in range(1, 5):
        if real_dict.get(pos) and palpite_dict.get(pos) == real_dict.get(pos):
            total += pontos_por_posicao[pos]

    return total


def calcular_pontuacao_participante(participante):
    """
    Calcula a pontuação total de um participante.
    Retorna dict com detalhamento.
    """
    pontos_jogos = 0
    pontos_classificacao = 0
    pontos_extras = 0
    jogos_pontuados = 0

    palpites = Palpite.objects.filter(participante=participante).select_related('jogo')
    for palpite in palpites:
        jogo = palpite.jogo
        if jogo.resultado_definido:
            pts = calcular_pontos_jogo(
                palpite.gols_casa, palpite.gols_fora,
                jogo.gols_casa, jogo.gols_fora,
                multiplicador_fase(jogo.fase)
            )
            if pts is not None:
                palpite.pontos = pts
                palpite.save(update_fields=['pontos'])
                pontos_jogos += pts
                jogos_pontuados += 1

    # Classificação dos grupos: usa o resultado oficial definido pelo admin
    resultados_oficiais = {}
    for rc in ResultadoClassificacao.objects.all():
        resultados_oficiais.setdefault(rc.grupo_id, {})[rc.posicao] = rc.selecao_id

    grupos = Grupo.objects.all()
    for grupo in grupos:
        real_dict = resultados_oficiais.get(grupo.id)
        if real_dict:
            pontos_classificacao += calcular_pontos_classificacao(
                participante, grupo, real_dict
            )

    # Palpites especiais (campeão, vice, 3º, pior): 20 pontos cada
    extras_oficiais = {re.tipo: re.selecao_id for re in ResultadoExtra.objects.all()}
    if extras_oficiais:
        palpites_extras = PalpiteExtra.objects.filter(participante=participante)
        for pe in palpites_extras:
            if extras_oficiais.get(pe.tipo) == pe.selecao_id:
                pontos_extras += PONTOS_EXTRA

    return {
        'total': pontos_jogos + pontos_classificacao + pontos_extras,
        'jogos': pontos_jogos,
        'classificacao': pontos_classificacao,
        'extras': pontos_extras,
        'jogos_pontuados': jogos_pontuados,
    }


def gerar_classificacao_geral():
    """
    Gera a classificação geral de todos os participantes.
    Retorna lista ordenada por pontuação total.
    """
    participantes = Participante.objects.all()
    classificacao = []

    for p in participantes:
        pontuacao = calcular_pontuacao_participante(p)
        classificacao.append({
            'participante': p,
            'pontos_total': pontuacao['total'],
            'pontos_jogos': pontuacao['jogos'],
            'pontos_classificacao': pontuacao['classificacao'],
            'pontos_extras': pontuacao['extras'],
            'jogos_pontuados': pontuacao['jogos_pontuados'],
        })

    classificacao.sort(key=lambda x: -x['pontos_total'])

    for idx, item in enumerate(classificacao):
        item['posicao'] = idx + 1

    return classificacao
