from .Distribuido import Carregamento_Distribuido

class Constante(Carregamento_Distribuido):
    def __init__(self, intensidade: float, posicao_inicial, posicao_final):
        self.intensidade = intensidade
        return super().__init__(posicao_inicial,posicao_final)