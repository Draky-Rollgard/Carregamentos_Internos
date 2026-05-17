from .operacoes import adicionar_apoio, adicionar_carga, listar_cargas
from .calculos import (
    resultante_cargas,
    momento_total_origem,
    calcular_reacoes_2_apoios,
    forca_cortante_em,
    gerar_diagrama_cortante,
    momento_fletor_em,
    gerar_diagrama_momento,
)


class Viga:
    def __init__(self, comprimento, referencial=0.0):
        comprimento = float(comprimento)
        if comprimento <= 0:
            raise ValueError("O comprimento da viga deve ser maior que zero.")
        self.comprimento = comprimento
        self.referencial = float(referencial)
        self.apoios = []
        self.cargas = []

    def validar_posicao(self, posicao):
        posicao = float(posicao)
        return 0 <= posicao <= self.comprimento

    def validar_intervalo(self, inicio, fim):
        inicio = float(inicio)
        fim = float(fim)
        return 0 <= inicio < fim <= self.comprimento

    def validar_carga(self, carga):
        if hasattr(carga, "posicao"):
            if not self.validar_posicao(carga.posicao):
                raise ValueError("Carga fora da viga.")
        if hasattr(carga, "posicao_inicial") and hasattr(carga, "posicao_final"):
            if not self.validar_intervalo(carga.posicao_inicial, carga.posicao_final):
                raise ValueError("Intervalo do carregamento fora da viga ou inválido.")
        return True

    def validar_estrutura(self):
        tipos = [apoio.__class__.__name__.lower() for apoio in self.apoios]

        if tipos.count("engaste") == 1 and len(tipos) == 1:
            return "engaste"

        if tipos.count("pino") == 1 and tipos.count("rolete") == 1 and len(tipos) == 2:
            if abs(self.apoios[0].posicao - self.apoios[1].posicao) < 1e-9:
                raise ValueError("Os apoios não podem estar na mesma posição.")
            return "pino_rolete"

        raise ValueError("Configuração inválida: use pino + rolete ou um único engaste.")

    def gerar_pontos_x(self, passo=0.01):
        passo = float(passo)
        if passo <= 0:
            passo = 0.01
        pontos = []
        x = 0.0
        while x < self.comprimento:
            pontos.append(round(x, 5))
            x += passo
        if not pontos or pontos[-1] != self.comprimento:
            pontos.append(round(self.comprimento, 5))
        return pontos

    def resetar(self, novo_comprimento=None):
        if novo_comprimento is not None:
            novo_comprimento = float(novo_comprimento)
            if novo_comprimento <= 0:
                raise ValueError("O comprimento da viga deve ser maior que zero.")
            self.comprimento = novo_comprimento
        self.apoios.clear()
        self.cargas.clear()


Viga.adicionar_apoio = adicionar_apoio
Viga.adicionar_carga = adicionar_carga
Viga.listar_cargas = listar_cargas
Viga.resultante_cargas = resultante_cargas
Viga.momento_total_origem = momento_total_origem
Viga.calcular_reacoes_2_apoios = calcular_reacoes_2_apoios
Viga.forca_cortante_em = forca_cortante_em
Viga.gerar_diagrama_cortante = gerar_diagrama_cortante
Viga.momento_fletor_em = momento_fletor_em
Viga.gerar_diagrama_momento = gerar_diagrama_momento