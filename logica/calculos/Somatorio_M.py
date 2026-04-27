from ..carregamentos import *

def momento_total_origem(self):
        """
        Soma momentos em x=0
        anti-horário positivo
        """
        M = 0

        for carga in self.cargas:

            # Concentrada
            if isinstance(carga, Carregamento_Concentrado):
                M -= carga.intensidade * carga.posicao

            # Distribuída constante
            elif isinstance(carga, Constante):
                L = carga.posicao_final - carga.posicao_inicial
                F = carga.intensidade * L
                xc = (carga.posicao_inicial + carga.posicao_final)/2
                M -= F * xc

            # Distribuída linear
            elif isinstance(carga, Linear):
                L = carga.posicao_final - carga.posicao_inicial
                q1 = carga.intensidade_inicial
                q2 = carga.intensidade_final

                F = (q1 + q2)/2 * L

                # centroide trapézio
                xc_local = L * (q1 + 2*q2) / (3*(q1 + q2))
                xc = carga.posicao_inicial + xc_local

                M -= F * xc

            # Momento concentrado
            elif isinstance(carga, Momento_Binario):
                M += carga.intensidade

        return M