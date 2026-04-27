from ..carregamentos import *

def resultante_cargas(self):
        """
        Soma todas as forças verticais aplicadas
        (positivo para baixo)
        """
        total = 0

        for carga in self.cargas:

            # Carga concentrada
            if isinstance(carga, Carregamento_Concentrado):
                total += carga.intensidade

            # Carga Distribuída constante
            elif isinstance(carga, Constante):
                L = carga.posicao_final - carga.posicao_inicial
                total += carga.intensidade * L

            # Carga Distribuída linear
            elif isinstance(carga, Linear):
                L = carga.posicao_final - carga.posicao_inicial
                area = (carga.intensidade_inicial + carga.intensidade_final)/2 * L
                total += area

        return total
