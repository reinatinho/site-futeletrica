from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from bolao.models import Jogo


JOGOS_16AVOS = [
    (73, '2026-06-28 16:00', '2º Grupo A x 2º Grupo B'),
    (74, '2026-06-29 13:00', 'Vencedor Grupo E x Melhor 3º (A/B/C/D/F)'),
    (75, '2026-06-29 16:00', 'Vencedor Grupo F x 2º Grupo C'),
    (76, '2026-06-29 19:00', 'Vencedor Grupo C x 2º Grupo F'),
    (77, '2026-06-30 13:00', 'Vencedor Grupo I x Melhor 3º (C/D/F/G/H)'),
    (78, '2026-06-30 16:00', '2º Grupo E x 2º Grupo I'),
    (79, '2026-06-30 19:00', 'Vencedor Grupo A x Melhor 3º (C/E/F/H/I)'),
    (80, '2026-07-01 13:00', 'Vencedor Grupo L x Melhor 3º (E/H/I/J/K)'),
    (81, '2026-07-01 16:00', 'Vencedor Grupo D x Melhor 3º (B/E/F/I/J)'),
    (82, '2026-07-01 19:00', 'Vencedor Grupo G x Melhor 3º (A/E/H/I/J)'),
    (83, '2026-07-02 13:00', '2º Grupo K x 2º Grupo L'),
    (84, '2026-07-02 16:00', 'Vencedor Grupo H x 2º Grupo J'),
    (85, '2026-07-02 19:00', 'Vencedor Grupo B x Melhor 3º (E/F/G/I/J)'),
    (86, '2026-07-03 13:00', 'Vencedor Grupo J x 2º Grupo H'),
    (87, '2026-07-03 16:00', 'Vencedor Grupo K x Melhor 3º (D/E/I/J/L)'),
    (88, '2026-07-03 19:00', '2º Grupo D x 2º Grupo G'),
]

JOGOS_OITAVAS = [
    (89, '2026-07-04 16:00', 'Vencedor Jogo 74 x Vencedor Jogo 77'),
    (90, '2026-07-04 19:00', 'Vencedor Jogo 73 x Vencedor Jogo 75'),
    (91, '2026-07-05 16:00', 'Vencedor Jogo 76 x Vencedor Jogo 78'),
    (92, '2026-07-05 19:00', 'Vencedor Jogo 79 x Vencedor Jogo 80'),
    (93, '2026-07-06 16:00', 'Vencedor Jogo 83 x Vencedor Jogo 84'),
    (94, '2026-07-06 19:00', 'Vencedor Jogo 81 x Vencedor Jogo 82'),
    (95, '2026-07-07 16:00', 'Vencedor Jogo 86 x Vencedor Jogo 88'),
    (96, '2026-07-07 19:00', 'Vencedor Jogo 85 x Vencedor Jogo 87'),
]

JOGOS_QUARTAS = [
    (97, '2026-07-09 16:00', 'Vencedor Jogo 89 x Vencedor Jogo 90'),
    (98, '2026-07-10 16:00', 'Vencedor Jogo 93 x Vencedor Jogo 94'),
    (99, '2026-07-12 16:00', 'Vencedor Jogo 91 x Vencedor Jogo 92'),
    (100, '2026-07-12 19:00', 'Vencedor Jogo 95 x Vencedor Jogo 96'),
]

JOGOS_SEMI = [
    (101, '2026-07-14 16:00', 'Vencedor Jogo 97 x Vencedor Jogo 98'),
    (102, '2026-07-15 16:00', 'Vencedor Jogo 99 x Vencedor Jogo 100'),
]

JOGOS_TERCEIRO = [
    (103, '2026-07-18 16:00', 'Perdedor Jogo 101 x Perdedor Jogo 102'),
]

JOGOS_FINAL = [
    (104, '2026-07-19 16:00', 'Vencedor Jogo 101 x Vencedor Jogo 102'),
]

FASES = [
    ('16avos', JOGOS_16AVOS),
    ('oitavas', JOGOS_OITAVAS),
    ('quartas', JOGOS_QUARTAS),
    ('semi', JOGOS_SEMI),
    ('terceiro', JOGOS_TERCEIRO),
    ('final', JOGOS_FINAL),
]


class Command(BaseCommand):
    help = 'Popula o banco com os jogos das fases eliminatórias da Copa 2026'

    def handle(self, *args, **options):
        self.stdout.write('Criando jogos das fases eliminatórias...')

        total = 0
        for fase, jogos in FASES:
            self.stdout.write(f'  Fase: {fase}')
            for numero, data_str, descricao in jogos:
                dt = timezone.make_aware(datetime.strptime(data_str, '%Y-%m-%d %H:%M'))
                Jogo.objects.update_or_create(
                    numero_jogo=numero,
                    defaults={
                        'fase': fase,
                        'data_hora': dt,
                        'descricao': descricao,
                        'rodada': 1,
                    }
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f'Seed concluído! {total} jogos eliminatórios criados.'))
