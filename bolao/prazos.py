"""Prazos de encerramento dos palpites por fase.

Após o prazo, o envio e o ajuste de palpites da fase ficam bloqueados
automaticamente (além do bloqueio manual feito pelo admin).
"""
from datetime import datetime
from django.utils import timezone

# Prazo de encerramento de cada fase (horário de São Paulo)
PRAZOS_STR = {
    'grupos': '2026-06-10 23:59',
    '16avos': '2026-06-27 23:59',
    'oitavas': '2026-07-03 23:59',
    'quartas': '2026-07-08 23:59',
    'semi': '2026-07-13 23:59',
    'terceiro': '2026-07-17 23:59',
    'final': '2026-07-18 23:59',
}

# Rótulo amigável para exibição
PRAZOS_LABEL = {
    'grupos': '10/06 às 23:59',
    '16avos': '27/06 às 23:59',
    'oitavas': '03/07 às 23:59',
    'quartas': '08/07 às 23:59',
    'semi': '13/07 às 23:59',
    'terceiro': '17/07 às 23:59',
    'final': '18/07 às 23:59',
}


def get_prazo(fase):
    """Retorna o datetime (aware) do prazo da fase, ou None."""
    s = PRAZOS_STR.get(fase)
    if not s:
        return None
    return timezone.make_aware(datetime.strptime(s, '%Y-%m-%d %H:%M'))


def prazo_passou(fase):
    """True se o prazo da fase já passou."""
    prazo = get_prazo(fase)
    return prazo is not None and timezone.now() > prazo


def prazo_label(fase):
    return PRAZOS_LABEL.get(fase, '')
