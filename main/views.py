from django.shortcuts import render

def home(request):
    """View para a página principal com informações gerais do Futeletrica"""
    context = {
        'titulo': 'Futeletrica 2013',
        'historia': """O grupo teve início em 2013, fundado por estudantes de engenharia elétrica da UFPR. O primeiro jogo, organizado por Eduardo Kesller, aconteceu na quadra da STARK às 23:00h. Ao longo dos anos, o grupo expandiu seu alcance, atraindo membros de diversas áreas e enriquecendo sua diversidade.

Em 2018, Renato Trevizan assumiu a administração, trazendo consigo novas ideias e entusiasmo. No ano seguinte, em 2019, Guilherme Cruz assumiu a presidência, liderando com determinação.

Em 2020, a diretoria de marketing foi oficialmente estabelecida, com Jimmy Antony encarregado de criar o perfil do Instagram para promover o grupo de maneira mais eficaz.

E em 2022, Renato Trevizan desenvolveu um programa em Python para realizar o sorteio dos times, proporcionando uma organização mais eficiente nos jogos. Em 2023, Pedro Mantovani criou o aplicativo do Futeletrica, com o apoio de Renato e Erik Nayan, realizando ajustes para melhorar a experiência dos membros do grupo.""",
        'regras': [
            'Respeite sempre seus companheiros de equipe e adversários.',
            'Não há árbitro, então todos devem ser honestos e fair play é essencial.',
            'Jogue com espírito esportivo, evite discussões e brigas.',
            'O jogo deve ser divertido para todos, independentemente do resultado.',
            'Mantenha-se seguro: evite jogadas perigosas e respeite as regras básicas do futebol.',
            'Não faça faltas intencionais, e se acontecerem, peça desculpas e jogue limpo.',
            'Aprecie a camaradagem e o espírito de equipe.',
            'Suspensão Temporária: Jogadores envolvidos em brigas podem ser suspensos por 1 a 2 jogos.',
            'Banimento: Jogadores reincidentes em brigas podem ser banidos dos jogos.',
            'Inclusão no grupo: É necessário ter no mínimo 3 partidas para entrar no grupo.',
            'Inclusão no ranking: É necessário ter no mínimo 5 partidas para aparecer no ranking.',
            'Lista de presença: qualquer integrante pode lançar a lista na segunda-feira após as 12:00h.',
            'Site: Jogadores recebem a escalação 1 dia antes do jogo através do link.',
            'Pontualidade: Chegue pelo menos 10 minutos antes do jogo.',
            'Após o jogo, celebre juntos, independentemente do resultado.',
            'Pagamento Mensalistas: devem ser realizados na 1ª semana do mês.',
            'Pagamento avulso: devem ser realizados após o jogo.',
            'Uniforme: Recomenda-se que cada jogador tenha as 3 camisas do grupo.'
        ]
    }
    return render(request, 'main/home.html', context)

def dashboard(request):
    """View para a página do dashboard com Power BI embeddado"""
    context = {
        'titulo': 'Dashboard - Futeletrica 2013',
        'powerbi_url': 'https://lookerstudio.google.com/embed/reporting/53e67754-5792-4797-a2d3-53598644d285/page/FCObF'
    }
    return render(request, 'main/dashboard.html', context)
