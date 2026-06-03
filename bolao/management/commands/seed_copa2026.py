from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from bolao.models import Grupo, Selecao, Jogo, ConfigBolao


GRUPOS_DATA = {
    'A': [
        ('México', 'MEX', '🇲🇽'),
        ('África do Sul', 'RSA', '🇿🇦'),
        ('Coreia do Sul', 'KOR', '🇰🇷'),
        ('Rep. Tcheca', 'CZE', '🇨🇿'),
    ],
    'B': [
        ('Canadá', 'CAN', '🇨🇦'),
        ('Bósnia', 'BIH', '🇧🇦'),
        ('Catar', 'QAT', '🇶🇦'),
        ('Suíça', 'SUI', '🇨🇭'),
    ],
    'C': [
        ('Brasil', 'BRA', '🇧🇷'),
        ('Marrocos', 'MAR', '🇲🇦'),
        ('Haiti', 'HAI', '🇭🇹'),
        ('Escócia', 'SCO', '🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f'),
    ],
    'D': [
        ('EUA', 'USA', '🇺🇸'),
        ('Paraguai', 'PAR', '🇵🇾'),
        ('Austrália', 'AUS', '🇦🇺'),
        ('Turquia', 'TUR', '🇹🇷'),
    ],
    'E': [
        ('Alemanha', 'GER', '🇩🇪'),
        ('Curaçau', 'CUW', '🇨🇼'),
        ('C. do Marfim', 'CIV', '🇨🇮'),
        ('Equador', 'ECU', '🇪🇨'),
    ],
    'F': [
        ('Holanda', 'NED', '🇳🇱'),
        ('Japão', 'JPN', '🇯🇵'),
        ('Suécia', 'SWE', '🇸🇪'),
        ('Tunísia', 'TUN', '🇹🇳'),
    ],
    'G': [
        ('Bélgica', 'BEL', '🇧🇪'),
        ('Egito', 'EGY', '🇪🇬'),
        ('Irã', 'IRN', '🇮🇷'),
        ('Nova Zelândia', 'NZL', '🇳🇿'),
    ],
    'H': [
        ('Espanha', 'ESP', '🇪🇸'),
        ('Cabo Verde', 'CPV', '🇨🇻'),
        ('Arábia Saudita', 'KSA', '🇸🇦'),
        ('Uruguai', 'URU', '🇺🇾'),
    ],
    'I': [
        ('França', 'FRA', '🇫🇷'),
        ('Senegal', 'SEN', '🇸🇳'),
        ('Iraque', 'IRQ', '🇮🇶'),
        ('Noruega', 'NOR', '🇳🇴'),
    ],
    'J': [
        ('Argentina', 'ARG', '🇦🇷'),
        ('Argélia', 'ALG', '🇩🇿'),
        ('Áustria', 'AUT', '🇦🇹'),
        ('Jordânia', 'JOR', '🇯🇴'),
    ],
    'K': [
        ('Portugal', 'POR', '🇵🇹'),
        ('Congo', 'COD', '🇨🇩'),
        ('Uzbequistão', 'UZB', '🇺🇿'),
        ('Colômbia', 'COL', '🇨🇴'),
    ],
    'L': [
        ('Inglaterra', 'ENG', '🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f'),
        ('Croácia', 'CRO', '🇭🇷'),
        ('Gana', 'GHA', '🇬🇭'),
        ('Panamá', 'PAN', '🇵🇦'),
    ],
}

JOGOS_DATA = [
    # Grupo A
    ('A', 'MEX', 'RSA', '2026-06-11 16:00'),
    ('A', 'KOR', 'CZE', '2026-06-11 23:00'),
    ('A', 'CZE', 'RSA', '2026-06-18 13:00'),
    ('A', 'MEX', 'KOR', '2026-06-18 22:00'),
    ('A', 'CZE', 'MEX', '2026-06-24 22:00'),
    ('A', 'RSA', 'KOR', '2026-06-24 22:00'),
    # Grupo B
    ('B', 'CAN', 'BIH', '2026-06-12 16:00'),
    ('B', 'QAT', 'SUI', '2026-06-13 16:00'),
    ('B', 'SUI', 'BIH', '2026-06-18 16:00'),
    ('B', 'CAN', 'QAT', '2026-06-18 19:00'),
    ('B', 'SUI', 'CAN', '2026-06-24 16:00'),
    ('B', 'BIH', 'QAT', '2026-06-24 16:00'),
    # Grupo C
    ('C', 'BRA', 'MAR', '2026-06-13 19:00'),
    ('C', 'HAI', 'SCO', '2026-06-13 22:00'),
    ('C', 'SCO', 'MAR', '2026-06-19 19:00'),
    ('C', 'BRA', 'HAI', '2026-06-19 21:30'),
    ('C', 'SCO', 'BRA', '2026-06-24 19:00'),
    ('C', 'MAR', 'HAI', '2026-06-24 19:00'),
    # Grupo D
    ('D', 'USA', 'PAR', '2026-06-12 22:00'),
    ('D', 'AUS', 'TUR', '2026-06-14 01:00'),
    ('D', 'TUR', 'PAR', '2026-06-20 01:00'),
    ('D', 'USA', 'AUS', '2026-06-19 16:00'),
    ('D', 'TUR', 'USA', '2026-06-25 23:00'),
    ('D', 'PAR', 'AUS', '2026-06-25 23:00'),
    # Grupo E
    ('E', 'GER', 'CUW', '2026-06-14 14:00'),
    ('E', 'CIV', 'ECU', '2026-06-14 20:00'),
    ('E', 'GER', 'CIV', '2026-06-20 17:00'),
    ('E', 'ECU', 'CUW', '2026-06-20 21:00'),
    ('E', 'ECU', 'GER', '2026-06-25 17:00'),
    ('E', 'CUW', 'CIV', '2026-06-25 17:00'),
    # Grupo F
    ('F', 'NED', 'JPN', '2026-06-14 17:00'),
    ('F', 'SWE', 'TUN', '2026-06-14 23:00'),
    ('F', 'TUN', 'JPN', '2026-06-21 01:00'),
    ('F', 'NED', 'SWE', '2026-06-20 14:00'),
    ('F', 'JPN', 'SWE', '2026-06-25 20:00'),
    ('F', 'TUN', 'NED', '2026-06-25 20:00'),
    # Grupo G
    ('G', 'BEL', 'EGY', '2026-06-15 16:00'),
    ('G', 'IRN', 'NZL', '2026-06-15 22:00'),
    ('G', 'BEL', 'IRN', '2026-06-21 16:00'),
    ('G', 'NZL', 'EGY', '2026-06-21 22:00'),
    ('G', 'EGY', 'IRN', '2026-06-27 00:00'),
    ('G', 'NZL', 'BEL', '2026-06-27 00:00'),
    # Grupo H
    ('H', 'ESP', 'CPV', '2026-06-15 13:00'),
    ('H', 'KSA', 'URU', '2026-06-15 19:00'),
    ('H', 'ESP', 'KSA', '2026-06-21 13:00'),
    ('H', 'URU', 'CPV', '2026-06-21 19:00'),
    ('H', 'CPV', 'KSA', '2026-06-26 21:00'),
    ('H', 'URU', 'ESP', '2026-06-26 21:00'),
    # Grupo I
    ('I', 'FRA', 'SEN', '2026-06-16 16:00'),
    ('I', 'IRQ', 'NOR', '2026-06-16 19:00'),
    ('I', 'FRA', 'IRQ', '2026-06-22 18:00'),
    ('I', 'NOR', 'SEN', '2026-06-22 21:00'),
    ('I', 'NOR', 'FRA', '2026-06-26 16:00'),
    ('I', 'SEN', 'IRQ', '2026-06-26 16:00'),
    # Grupo J
    ('J', 'ARG', 'ALG', '2026-06-16 22:00'),
    ('J', 'AUT', 'JOR', '2026-06-17 01:00'),
    ('J', 'ARG', 'AUT', '2026-06-22 14:00'),
    ('J', 'JOR', 'ALG', '2026-06-23 00:00'),
    ('J', 'ALG', 'AUT', '2026-06-27 23:00'),
    ('J', 'JOR', 'ARG', '2026-06-27 23:00'),
    # Grupo K
    ('K', 'POR', 'COD', '2026-06-17 14:00'),
    ('K', 'UZB', 'COL', '2026-06-17 23:00'),
    ('K', 'POR', 'UZB', '2026-06-23 14:00'),
    ('K', 'COL', 'COD', '2026-06-23 23:00'),
    ('K', 'COL', 'POR', '2026-06-27 20:30'),
    ('K', 'COD', 'UZB', '2026-06-27 20:30'),
    # Grupo L
    ('L', 'ENG', 'CRO', '2026-06-17 17:00'),
    ('L', 'GHA', 'PAN', '2026-06-17 20:00'),
    ('L', 'ENG', 'GHA', '2026-06-23 17:00'),
    ('L', 'PAN', 'CRO', '2026-06-23 20:00'),
    ('L', 'PAN', 'ENG', '2026-06-27 18:00'),
    ('L', 'CRO', 'GHA', '2026-06-27 18:00'),
]


class Command(BaseCommand):
    help = 'Popula o banco com os dados da Copa do Mundo 2026 (fase de grupos)'

    def handle(self, *args, **options):
        self.stdout.write('Limpando dados anteriores...')
        Jogo.objects.filter(fase='grupos').delete()
        Selecao.objects.all().delete()
        Grupo.objects.all().delete()

        self.stdout.write('Criando grupos e seleções...')
        grupos_obj = {}
        selecoes_obj = {}

        for letra, selecoes in GRUPOS_DATA.items():
            grupo = Grupo.objects.create(letra=letra, nome=f'Grupo {letra}')
            grupos_obj[letra] = grupo

            for nome, codigo, emoji in selecoes:
                sel = Selecao.objects.create(
                    nome=nome,
                    codigo=codigo,
                    bandeira_emoji=emoji,
                    grupo=grupo,
                )
                selecoes_obj[codigo] = sel

        self.stdout.write(f'  Criados {len(grupos_obj)} grupos e {len(selecoes_obj)} seleções')

        self.stdout.write('Criando jogos...')
        rodada_counter = {}
        for grupo_letra, casa_cod, fora_cod, data_str in JOGOS_DATA:
            grupo = grupos_obj[grupo_letra]
            key = grupo_letra
            rodada_counter[key] = rodada_counter.get(key, 0) + 1
            rodada = (rodada_counter[key] + 1) // 2  # 2 jogos por rodada

            dt = timezone.make_aware(datetime.strptime(data_str, '%Y-%m-%d %H:%M'))

            Jogo.objects.create(
                grupo=grupo,
                selecao_casa=selecoes_obj[casa_cod],
                selecao_fora=selecoes_obj[fora_cod],
                data_hora=dt,
                rodada=rodada,
                fase='grupos',
            )

        total_jogos = Jogo.objects.filter(fase='grupos').count()
        self.stdout.write(f'  Criados {total_jogos} jogos')

        ConfigBolao.get_config()
        self.stdout.write(self.style.SUCCESS(
            f'Seed concluído! {len(grupos_obj)} grupos, {len(selecoes_obj)} seleções, {total_jogos} jogos.'
        ))
