from .Distribuido import Carregamento_Distribuido

class Linear(Carregamento_Distribuido):
    def __init__(self, intensidade_inicial: float, intensidade_final: float, posicao_inicial, posicao_final):
        self.intensidade_inicial = intensidade_inicial
        self.intensidade_final = intensidade_final
        return super().__init__(posicao_inicial,posicao_final)