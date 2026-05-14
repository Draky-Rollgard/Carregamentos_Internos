from ..carregamentos import *

def calcular_reacoes_2_apoios(self):
    """
        Caso simples:
        1 pino + 1 rolete
        reações verticais Ay e By
    """

    if len(self.apoios) != 2:
        print("Necessário exatamente 2 apoios.")
        return

    A = self.apoios[0].posicao
    B = self.apoios[1].posicao
    
    if A == B:
        raise ValueError("Os apoios não podem ocupar a mesma posição.")

    soma_forcas = self.resultante_cargas()
    soma_momentos_A = 0

    for carga in self.cargas:

        if isinstance(carga, Carregamento_Concentrado):
            soma_momentos_A -= carga.intensidade * (carga.posicao - A)

        elif isinstance(carga, Constante):
            L = carga.posicao_final - carga.posicao_inicial
            F = carga.intensidade * L
            xc = (carga.posicao_inicial + carga.posicao_final)/2
            soma_momentos_A -= F * (xc - A)

        elif isinstance(carga, Linear):
            L = carga.posicao_final - carga.posicao_inicial
            q1 = carga.intensidade_inicial
            q2 = carga.intensidade_final

            F = (q1 + q2)/2 * L
            xc_local = L * (q1 + 2*q2)/(3*(q1 + q2))
            xc = carga.posicao_inicial + xc_local

            soma_momentos_A -= F * (xc - A)

        elif isinstance(carga, Momento_Binario):
            soma_momentos_A += carga.intensidade

    # ΣM(A)=0
    By = -soma_momentos_A / (B - A)

    # ΣFy=0
    Ay = soma_forcas - By

    return {
        "Ay": Ay,
        "By": By
    }