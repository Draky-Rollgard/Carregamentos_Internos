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
        referencial = float(referencial)

        if comprimento <= 0:
            raise ValueError("O comprimento da viga deve ser maior que zero.")

        if not 0 <= referencial <= comprimento:
            raise ValueError("O referencial deve estar dentro do comprimento total da viga.")

        self.comprimento = comprimento
        self.referencial = referencial
        self.apoios = []
        self.cargas = []

    # ==========================================================
    # Conversões de referencial
    # ==========================================================
    def posicao_para_interna(self, posicao_referencial):
        """Converte a posição digitada pelo usuário para o eixo interno 0..L."""
        return float(posicao_referencial) + self.referencial

    def posicao_para_referencial(self, posicao_interna):
        """Converte uma posição interna 0..L para o eixo escolhido pelo usuário."""
        return float(posicao_interna) - self.referencial

    def intervalo_para_interno(self, inicio_referencial, fim_referencial):
        """Converte um intervalo digitado no referencial para posições internas."""
        return (
            self.posicao_para_interna(inicio_referencial),
            self.posicao_para_interna(fim_referencial),
        )

    def limites_referencial(self):
        """Retorna o intervalo de posições válido para entrada do usuário."""
        return -self.referencial, self.comprimento - self.referencial

    def validar_posicao_referencial(self, posicao_referencial):
        posicao_interna = self.posicao_para_interna(posicao_referencial)
        if not self.validar_posicao(posicao_interna):
            minimo, maximo = self.limites_referencial()
            raise ValueError(
                f"Posição fora da viga. Informe um valor entre {minimo:g} e {maximo:g}."
            )
        return posicao_interna

    def validar_intervalo_referencial(self, inicio_referencial, fim_referencial):
        inicio_interno, fim_interno = self.intervalo_para_interno(
            inicio_referencial,
            fim_referencial,
        )
        if not self.validar_intervalo(inicio_interno, fim_interno):
            minimo, maximo = self.limites_referencial()
            raise ValueError(
                "Intervalo do carregamento fora da viga ou inválido. "
                f"Informe posições entre {minimo:g} e {maximo:g}, com início menor que o fim."
            )
        return inicio_interno, fim_interno

    # ==========================================================
    # Validações físicas no eixo interno da viga
    # ==========================================================
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

    def resetar(self, novo_comprimento=None, novo_referencial=None):
        if novo_comprimento is not None:
            novo_comprimento = float(novo_comprimento)
            if novo_comprimento <= 0:
                raise ValueError("O comprimento da viga deve ser maior que zero.")
            self.comprimento = novo_comprimento

        if novo_referencial is not None:
            novo_referencial = float(novo_referencial)
            if not 0 <= novo_referencial <= self.comprimento:
                raise ValueError("O referencial deve estar dentro do comprimento total da viga.")
            self.referencial = novo_referencial

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
