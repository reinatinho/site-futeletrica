import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import (
    Participante, Grupo, Selecao, Jogo,
    Palpite, PalpiteClassificacao, PalpiteExtra, ConfigBolao
)
from .forms import LoginForm, CadastroForm
from .pontuacao import gerar_classificacao_geral, calcular_pontos_jogo


def get_participante(request):
    participante_id = request.session.get('participante_id')
    if participante_id:
        try:
            return Participante.objects.get(id=participante_id)
        except Participante.DoesNotExist:
            del request.session['participante_id']
    return None


def login_view(request):
    participante = get_participante(request)
    if participante:
        return redirect('bolao:home')

    login_form = LoginForm()
    cadastro_form = CadastroForm()
    show_cadastro = False
    show_pix_modal = False

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username'].strip().lower()
                pin = login_form.cleaned_data['pin']
                try:
                    p = Participante.objects.get(username=username)
                    if p.check_pin(pin):
                        request.session['participante_id'] = p.id
                        return redirect('bolao:palpites')
                    else:
                        messages.error(request, 'Usuário ou PIN incorreto.')
                except Participante.DoesNotExist:
                    messages.error(request, 'Usuário ou PIN incorreto.')

        elif action == 'cadastro':
            cadastro_form = CadastroForm(request.POST)
            show_cadastro = True
            if cadastro_form.is_valid():
                p = Participante(
                    username=cadastro_form.cleaned_data['username'],
                    nome=cadastro_form.cleaned_data['nome'].strip().title(),
                    sobrenome=cadastro_form.cleaned_data['sobrenome'].strip().title(),
                )
                p.set_pin(cadastro_form.cleaned_data['pin'])
                p.save()
                request.session['participante_id'] = p.id
                show_pix_modal = True
                show_cadastro = False

    return render(request, 'bolao/login.html', {
        'login_form': login_form,
        'cadastro_form': cadastro_form,
        'show_cadastro': show_cadastro,
        'show_pix_modal': show_pix_modal,
    })


def logout_view(request):
    request.session.pop('participante_id', None)
    return redirect('bolao:home')


def palpites_view(request):
    participante = get_participante(request)
    if not participante:
        return redirect('bolao:login')

    config = ConfigBolao.get_config()
    if not config.fase_grupos_aberta:
        messages.info(request, 'Os palpites da fase de grupos estão fechados.')

    grupos = Grupo.objects.prefetch_related(
        'selecoes', 'jogos', 'jogos__selecao_casa', 'jogos__selecao_fora'
    ).all()

    palpites_existentes = {}
    for p in Palpite.objects.filter(participante=participante):
        palpites_existentes[p.jogo_id] = {
            'gols_casa': p.gols_casa,
            'gols_fora': p.gols_fora,
            'pontos': p.pontos,
        }

    classificacoes_existentes = {}
    for pc in PalpiteClassificacao.objects.filter(participante=participante):
        if pc.grupo_id not in classificacoes_existentes:
            classificacoes_existentes[pc.grupo_id] = {}
        classificacoes_existentes[pc.grupo_id][pc.posicao] = pc.selecao_id

    extras_existentes = {}
    for pe in PalpiteExtra.objects.filter(participante=participante):
        extras_existentes[pe.tipo] = pe.selecao_id

    todas_selecoes = list(Selecao.objects.values('id', 'nome', 'bandeira_emoji', 'codigo', 'grupo_id'))

    fase_grupos_bloqueada = config.lock_fase_grupos

    todas_fases_elim = []
    fase_elim_map = [
        ('16avos', config.fase_16avos_aberta, '16-avos de Final', config.lock_16avos),
        ('oitavas', config.fase_oitavas_aberta, 'Oitavas de Final', config.lock_oitavas),
        ('quartas', config.fase_quartas_aberta, 'Quartas de Final', config.lock_quartas),
        ('semi', config.fase_semi_aberta, 'Semifinais', config.lock_semi),
        ('terceiro', config.fase_terceiro_aberta, 'Disputa 3º Lugar', config.lock_terceiro),
        ('final', config.fase_final_aberta, 'Final', config.lock_final),
    ]

    for fase_cod, aberta, fase_nome, bloqueada in fase_elim_map:
        jogos = Jogo.objects.filter(fase=fase_cod).select_related(
            'selecao_casa', 'selecao_fora'
        )
        if jogos.exists():
            todas_fases_elim.append({
                'codigo': fase_cod,
                'nome': fase_nome,
                'aberta': aberta,
                'bloqueada': bloqueada,
                'jogos': jogos,
            })

    palpites_elim_existentes = {}
    for p in Palpite.objects.filter(
        participante=participante,
        jogo__fase__in=['16avos', 'oitavas', 'quartas', 'semi', 'terceiro', 'final']
    ):
        palpites_elim_existentes[p.jogo_id] = {
            'gols_casa': p.gols_casa,
            'gols_fora': p.gols_fora,
            'pontos': p.pontos,
        }

    return render(request, 'bolao/palpites.html', {
        'participante': participante,
        'grupos': grupos,
        'palpites_existentes': json.dumps(palpites_existentes),
        'classificacoes_existentes': json.dumps(classificacoes_existentes),
        'extras_existentes': json.dumps(extras_existentes),
        'todas_selecoes': json.dumps(todas_selecoes),
        'config': config,
        'fase_grupos_bloqueada': fase_grupos_bloqueada,
        'todas_fases_elim': todas_fases_elim,
        'palpites_elim_existentes': json.dumps(palpites_elim_existentes),
    })


@require_POST
def salvar_palpites(request):
    participante = get_participante(request)
    if not participante:
        return JsonResponse({'error': 'Não autenticado'}, status=401)

    config = ConfigBolao.get_config()
    if not config.fase_grupos_aberta:
        return JsonResponse({'error': 'Palpites da fase de grupos estão fechados'}, status=403)

    if config.lock_fase_grupos:
        return JsonResponse({'error': 'A fase de grupos está bloqueada. Não é possível enviar ou editar palpites.'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    palpites_data = data.get('palpites', {})
    classificacoes_data = data.get('classificacoes', {})
    extras_data = data.get('extras', {})

    for jogo_id_str, valores in palpites_data.items():
        jogo_id = int(jogo_id_str)
        gols_casa = valores.get('gols_casa')
        gols_fora = valores.get('gols_fora')

        if gols_casa is not None and gols_fora is not None:
            Palpite.objects.update_or_create(
                participante=participante,
                jogo_id=jogo_id,
                defaults={
                    'gols_casa': int(gols_casa),
                    'gols_fora': int(gols_fora),
                }
            )

    for grupo_id_str, posicoes in classificacoes_data.items():
        grupo_id = int(grupo_id_str)
        for posicao_str, selecao_id in posicoes.items():
            if selecao_id:
                PalpiteClassificacao.objects.update_or_create(
                    participante=participante,
                    grupo_id=grupo_id,
                    posicao=int(posicao_str),
                    defaults={'selecao_id': int(selecao_id)}
                )

    for tipo, selecao_id in extras_data.items():
        if selecao_id:
            PalpiteExtra.objects.update_or_create(
                participante=participante,
                tipo=tipo,
                defaults={'selecao_id': int(selecao_id)}
            )

    return JsonResponse({'success': True, 'message': 'Palpites salvos com sucesso!'})


def home_view(request):
    """Página principal do bolão com classificação geral."""
    participante = get_participante(request)
    config = ConfigBolao.get_config()
    classificacao = gerar_classificacao_geral()

    jogos_com_resultado = Jogo.objects.filter(
        gols_casa__isnull=False, gols_fora__isnull=False
    ).count()
    total_jogos = Jogo.objects.count()

    return render(request, 'bolao/home.html', {
        'participante': participante,
        'classificacao': classificacao,
        'config': config,
        'jogos_com_resultado': jogos_com_resultado,
        'total_jogos': total_jogos,
    })


def palpites_publicos_view(request):
    """Página pública com todos os palpites (após liberação pelo admin)."""
    config = ConfigBolao.get_config()

    alguma_fase_publica = (
        config.publico_fase_grupos or config.publico_16avos or
        config.publico_oitavas or config.publico_quartas or
        config.publico_semi or config.publico_terceiro or config.publico_final
    )
    if not alguma_fase_publica:
        messages.info(request, 'Os palpites públicos ainda não foram liberados.')
        return redirect('bolao:home')

    participantes = Participante.objects.all()
    grupos = Grupo.objects.prefetch_related(
        'jogos', 'jogos__selecao_casa', 'jogos__selecao_fora'
    ).all()

    fases_elim_publicas = []
    fase_publico_map = [
        ('16avos', config.publico_16avos, '16-avos de Final'),
        ('oitavas', config.publico_oitavas, 'Oitavas de Final'),
        ('quartas', config.publico_quartas, 'Quartas de Final'),
        ('semi', config.publico_semi, 'Semifinais'),
        ('terceiro', config.publico_terceiro, 'Disputa 3º Lugar'),
        ('final', config.publico_final, 'Final'),
    ]
    for fase_cod, publico, fase_nome in fase_publico_map:
        if publico:
            jogos = Jogo.objects.filter(
                fase=fase_cod, selecao_casa__isnull=False, selecao_fora__isnull=False
            ).select_related('selecao_casa', 'selecao_fora')
            if jogos.exists():
                fases_elim_publicas.append({
                    'codigo': fase_cod,
                    'nome': fase_nome,
                    'jogos': jogos,
                })

    dados_participantes = []
    for p in participantes:
        palpites = {}
        for palpite in Palpite.objects.filter(participante=p).select_related('jogo'):
            palpites[palpite.jogo_id] = {
                'casa': palpite.gols_casa,
                'fora': palpite.gols_fora,
                'pontos': palpite.pontos,
            }
        dados_participantes.append({
            'participante': p,
            'palpites': palpites,
        })

    return render(request, 'bolao/publico.html', {
        'participantes': dados_participantes,
        'grupos': grupos,
        'fases_elim_publicas': fases_elim_publicas,
        'config': config,
    })


# ===== ADMIN VIEWS =====

ADMIN_PASSWORD = 'Limonadadonorte@2026'

def admin_required(view_func):
    """Decorator para verificar acesso admin."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('bolao_admin'):
            return redirect('bolao:admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login_view(request):
    if request.session.get('bolao_admin'):
        return redirect('bolao:admin_painel')

    if request.method == 'POST':
        senha = request.POST.get('senha', '')
        if senha == ADMIN_PASSWORD:
            request.session['bolao_admin'] = True
            return redirect('bolao:admin_painel')
        else:
            messages.error(request, 'Senha de admin incorreta.')

    return render(request, 'bolao/admin_login.html')


@admin_required
def admin_painel_view(request):
    config = ConfigBolao.get_config()
    participantes = Participante.objects.all()

    total_participantes = participantes.count()
    total_jogos = Jogo.objects.count()

    participantes_status = []
    for p in participantes:
        palpites_feitos = Palpite.objects.filter(participante=p).count()
        participantes_status.append({
            'participante': p,
            'palpites_feitos': palpites_feitos,
            'total_esperado': total_jogos,
            'completo': palpites_feitos >= total_jogos,
            'percentual': round(palpites_feitos / total_jogos * 100) if total_jogos else 0,
        })

    participantes_status.sort(key=lambda x: -x['palpites_feitos'])

    completos = sum(1 for p in participantes_status if p['completo'])
    pendentes = total_participantes - completos

    grupos = Grupo.objects.prefetch_related(
        'jogos', 'jogos__selecao_casa', 'jogos__selecao_fora'
    ).all()

    fases_elim = []
    for fase_cod, fase_nome in Jogo.FASE_CHOICES:
        if fase_cod == 'grupos':
            continue
        jogos = Jogo.objects.filter(
            fase=fase_cod, selecao_casa__isnull=False, selecao_fora__isnull=False
        ).select_related('selecao_casa', 'selecao_fora')
        if jogos.exists():
            fases_elim.append({
                'codigo': fase_cod,
                'nome': fase_nome,
                'jogos': jogos,
            })

    return render(request, 'bolao/admin_painel.html', {
        'config': config,
        'participantes_status': participantes_status,
        'total_participantes': total_participantes,
        'completos': completos,
        'pendentes': pendentes,
        'grupos': grupos,
        'fases_elim': fases_elim,
    })


@admin_required
@require_POST
def admin_salvar_resultado(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    jogo_id = data.get('jogo_id')
    gols_casa = data.get('gols_casa')
    gols_fora = data.get('gols_fora')

    if jogo_id is None or gols_casa is None or gols_fora is None:
        return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

    try:
        jogo = Jogo.objects.get(id=jogo_id)
    except Jogo.DoesNotExist:
        return JsonResponse({'error': 'Jogo não encontrado'}, status=404)

    jogo.gols_casa = int(gols_casa)
    jogo.gols_fora = int(gols_fora)
    jogo.save()

    # Recalcular pontos dos palpites deste jogo
    palpites = Palpite.objects.filter(jogo=jogo)
    for palpite in palpites:
        pts = calcular_pontos_jogo(
            palpite.gols_casa, palpite.gols_fora,
            jogo.gols_casa, jogo.gols_fora
        )
        palpite.pontos = pts
        palpite.save(update_fields=['pontos'])

    return JsonResponse({
        'success': True,
        'message': f'Resultado salvo: {jogo.selecao_casa} {gols_casa} x {gols_fora} {jogo.selecao_fora}',
        'palpites_atualizados': palpites.count(),
    })


@admin_required
@require_POST
def admin_salvar_config(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    config = ConfigBolao.get_config()

    campos_bool = [
        'fase_grupos_aberta', 'fase_16avos_aberta', 'fase_oitavas_aberta',
        'fase_quartas_aberta', 'fase_semi_aberta', 'fase_terceiro_aberta',
        'fase_final_aberta', 'palpites_publicos',
        'publico_fase_grupos', 'publico_16avos', 'publico_oitavas',
        'publico_quartas', 'publico_semi', 'publico_terceiro', 'publico_final',
        'lock_fase_grupos', 'lock_16avos', 'lock_oitavas',
        'lock_quartas', 'lock_semi', 'lock_terceiro', 'lock_final',
    ]

    for campo in campos_bool:
        if campo in data:
            setattr(config, campo, bool(data[campo]))

    config.save()
    return JsonResponse({'success': True, 'message': 'Configurações atualizadas!'})


def palpites_eliminatorias_view(request):
    """Palpites das fases eliminatórias."""
    participante = get_participante(request)
    if not participante:
        return redirect('bolao:login')

    config = ConfigBolao.get_config()

    fases_disponiveis = []
    fase_map = [
        ('16avos', config.fase_16avos_aberta, '16-avos de Final', config.lock_16avos),
        ('oitavas', config.fase_oitavas_aberta, 'Oitavas de Final', config.lock_oitavas),
        ('quartas', config.fase_quartas_aberta, 'Quartas de Final', config.lock_quartas),
        ('semi', config.fase_semi_aberta, 'Semifinais', config.lock_semi),
        ('terceiro', config.fase_terceiro_aberta, 'Disputa 3º Lugar', config.lock_terceiro),
        ('final', config.fase_final_aberta, 'Final', config.lock_final),
    ]

    for fase_cod, aberta, fase_nome, bloqueada in fase_map:
        jogos = Jogo.objects.filter(fase=fase_cod, selecao_casa__isnull=False, selecao_fora__isnull=False).select_related(
            'selecao_casa', 'selecao_fora'
        )
        if jogos.exists():
            fases_disponiveis.append({
                'codigo': fase_cod,
                'nome': fase_nome,
                'aberta': aberta,
                'bloqueada': bloqueada,
                'jogos': jogos,
            })

    palpites_existentes = {}
    for p in Palpite.objects.filter(participante=participante, jogo__fase__in=['16avos', 'oitavas', 'quartas', 'semi', 'terceiro', 'final']):
        palpites_existentes[p.jogo_id] = {
            'gols_casa': p.gols_casa,
            'gols_fora': p.gols_fora,
            'pontos': p.pontos,
        }

    return render(request, 'bolao/palpites_eliminatorias.html', {
        'participante': participante,
        'fases_disponiveis': fases_disponiveis,
        'palpites_existentes': json.dumps(palpites_existentes),
        'config': config,
    })


@require_POST
def salvar_palpites_eliminatorias(request):
    """Salvar palpites das fases eliminatórias."""
    participante = get_participante(request)
    if not participante:
        return JsonResponse({'error': 'Não autenticado'}, status=401)

    config = ConfigBolao.get_config()

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    palpites_data = data.get('palpites', {})

    fase_aberta_map = {
        '16avos': config.fase_16avos_aberta,
        'oitavas': config.fase_oitavas_aberta,
        'quartas': config.fase_quartas_aberta,
        'semi': config.fase_semi_aberta,
        'terceiro': config.fase_terceiro_aberta,
        'final': config.fase_final_aberta,
    }

    fase_lock_map = {
        '16avos': config.lock_16avos,
        'oitavas': config.lock_oitavas,
        'quartas': config.lock_quartas,
        'semi': config.lock_semi,
        'terceiro': config.lock_terceiro,
        'final': config.lock_final,
    }

    for jogo_id_str, valores in palpites_data.items():
        jogo_id = int(jogo_id_str)
        gols_casa = valores.get('gols_casa')
        gols_fora = valores.get('gols_fora')

        if gols_casa is not None and gols_fora is not None:
            try:
                jogo = Jogo.objects.get(id=jogo_id)
            except Jogo.DoesNotExist:
                continue

            if not fase_aberta_map.get(jogo.fase, False):
                continue

            if fase_lock_map.get(jogo.fase, False):
                continue

            if not jogo.equipes_definidas:
                continue

            Palpite.objects.update_or_create(
                participante=participante,
                jogo_id=jogo_id,
                defaults={
                    'gols_casa': int(gols_casa),
                    'gols_fora': int(gols_fora),
                }
            )

    return JsonResponse({'success': True, 'message': 'Palpites salvos com sucesso!'})


@admin_required
@require_POST
def admin_definir_equipes(request):
    """Admin define as equipes de um jogo eliminatório."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    jogo_id = data.get('jogo_id')
    selecao_casa_id = data.get('selecao_casa_id')
    selecao_fora_id = data.get('selecao_fora_id')

    if not jogo_id:
        return JsonResponse({'error': 'ID do jogo obrigatório'}, status=400)

    try:
        jogo = Jogo.objects.get(id=jogo_id)
    except Jogo.DoesNotExist:
        return JsonResponse({'error': 'Jogo não encontrado'}, status=404)

    if jogo.fase == 'grupos':
        return JsonResponse({'error': 'Não é possível alterar jogos da fase de grupos'}, status=400)

    if selecao_casa_id:
        jogo.selecao_casa_id = int(selecao_casa_id)
    else:
        jogo.selecao_casa = None

    if selecao_fora_id:
        jogo.selecao_fora_id = int(selecao_fora_id)
    else:
        jogo.selecao_fora = None

    jogo.save()

    return JsonResponse({
        'success': True,
        'message': f'Equipes definidas para Jogo {jogo.numero_jogo}',
    })


@admin_required
def admin_eliminatorias_view(request):
    """Admin: gerenciar jogos eliminatórios."""
    config = ConfigBolao.get_config()
    selecoes = Selecao.objects.all().order_by('nome')

    fases = []
    for fase_cod, fase_nome in Jogo.FASE_CHOICES:
        if fase_cod == 'grupos':
            continue
        jogos = Jogo.objects.filter(fase=fase_cod).select_related('selecao_casa', 'selecao_fora')
        if jogos.exists():
            fases.append({
                'codigo': fase_cod,
                'nome': fase_nome,
                'jogos': jogos,
            })

    todas_selecoes = list(Selecao.objects.values('id', 'nome', 'bandeira_emoji', 'codigo').order_by('nome'))

    return render(request, 'bolao/admin_eliminatorias.html', {
        'config': config,
        'fases': fases,
        'todas_selecoes': json.dumps(todas_selecoes),
    })


@admin_required
def admin_logout_view(request):
    request.session.pop('bolao_admin', None)
    return redirect('bolao:home')
