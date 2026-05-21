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
        return redirect('bolao:palpites')

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
    return redirect('bolao:login')


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

    todas_selecoes = list(Selecao.objects.values('id', 'nome', 'bandeira_emoji', 'grupo_id'))

    return render(request, 'bolao/palpites.html', {
        'participante': participante,
        'grupos': grupos,
        'palpites_existentes': json.dumps(palpites_existentes),
        'classificacoes_existentes': json.dumps(classificacoes_existentes),
        'extras_existentes': json.dumps(extras_existentes),
        'todas_selecoes': json.dumps(todas_selecoes),
        'config': config,
    })


@require_POST
def salvar_palpites(request):
    participante = get_participante(request)
    if not participante:
        return JsonResponse({'error': 'Não autenticado'}, status=401)

    config = ConfigBolao.get_config()
    if not config.fase_grupos_aberta:
        return JsonResponse({'error': 'Palpites da fase de grupos estão fechados'}, status=403)

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
