import hashlib
from django.db import models


class Participante(models.Model):
    username = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    pin_hash = models.CharField(max_length=64)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome', 'sobrenome']

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    def set_pin(self, pin):
        self.pin_hash = hashlib.sha256(pin.encode()).hexdigest()

    def check_pin(self, pin):
        return self.pin_hash == hashlib.sha256(pin.encode()).hexdigest()

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"


class Grupo(models.Model):
    letra = models.CharField(max_length=1, unique=True)
    nome = models.CharField(max_length=20)

    class Meta:
        ordering = ['letra']

    def __str__(self):
        return f"Grupo {self.letra}"


class Selecao(models.Model):
    nome = models.CharField(max_length=60)
    codigo = models.CharField(max_length=3, unique=True)
    bandeira_emoji = models.CharField(max_length=10, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='selecoes')

    class Meta:
        verbose_name = 'Seleção'
        verbose_name_plural = 'Seleções'
        ordering = ['grupo', 'nome']

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='jogos')
    selecao_casa = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='jogos_casa')
    selecao_fora = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='jogos_fora')
    data_hora = models.DateTimeField()
    rodada = models.PositiveSmallIntegerField(default=1)
    fase = models.CharField(max_length=20, default='grupos')

    gols_casa = models.PositiveSmallIntegerField(null=True, blank=True)
    gols_fora = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['data_hora']
        verbose_name = 'Jogo'

    def __str__(self):
        return f"{self.selecao_casa} x {self.selecao_fora} ({self.data_hora.strftime('%d/%m')})"

    @property
    def resultado_definido(self):
        return self.gols_casa is not None and self.gols_fora is not None


class Palpite(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='palpites')
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='palpites')
    gols_casa = models.PositiveSmallIntegerField(null=True, blank=True)
    gols_fora = models.PositiveSmallIntegerField(null=True, blank=True)
    pontos = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['participante', 'jogo']
        ordering = ['jogo__data_hora']

    def __str__(self):
        return f"{self.participante} - {self.jogo}"


class PalpiteClassificacao(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='palpites_classificacao')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    selecao = models.ForeignKey(Selecao, on_delete=models.CASCADE)
    posicao = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ['participante', 'grupo', 'posicao']
        ordering = ['grupo', 'posicao']

    def __str__(self):
        return f"{self.participante} - Grupo {self.grupo.letra} - {self.posicao}º: {self.selecao}"


class PalpiteExtra(models.Model):
    TIPO_CHOICES = [
        ('campeao', 'Campeão'),
        ('vice', 'Vice-Campeão'),
        ('terceiro', 'Terceiro Colocado'),
        ('pior', 'Pior Seleção'),
    ]

    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='palpites_extras')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    selecao = models.ForeignKey(Selecao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['participante', 'tipo']

    def __str__(self):
        return f"{self.participante} - {self.get_tipo_display()}: {self.selecao}"


class ConfigBolao(models.Model):
    fase_grupos_aberta = models.BooleanField(default=True)
    prazo_fase_grupos = models.DateTimeField(null=True, blank=True)
    fase_16avos_aberta = models.BooleanField(default=False)
    fase_oitavas_aberta = models.BooleanField(default=False)
    fase_quartas_aberta = models.BooleanField(default=False)
    fase_semi_aberta = models.BooleanField(default=False)
    fase_terceiro_aberta = models.BooleanField(default=False)
    fase_final_aberta = models.BooleanField(default=False)
    palpites_publicos = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Configuração do Bolão'
        verbose_name_plural = 'Configurações do Bolão'

    def __str__(self):
        return "Configuração do Bolão"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config
