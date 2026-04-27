from .Apoio import Apoio

class pino(Apoio): # apoio fixo de grau 2, restringe Fx e Fy
    def __init__(self,posicao):
        return super().__init__(posicao)