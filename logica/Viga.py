from .operacoes import *
from .calculos import *
class Viga:
    def __init__(self, comprimento):
        self.comprimento = comprimento
        self.apoios = []
        self.cargas = []

Viga.adicionar_apoio = adicionar_apoio
Viga.adicionar_carga = adicionar_carga
Viga.listar_cargas = listar_cargas
Viga.resultante_cargas = resultante_cargas
Viga.momento_total_origem = momento_total_origem
Viga.calcular_reacoes_2_apoios = calcular_reacoes_2_apoios