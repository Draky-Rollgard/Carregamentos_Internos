from .Apoio import Apoio

class rolete(Apoio): # apoio móvel de grau 1, restringe Fy
    def __init__(self,posicao):
        return super().__init__(posicao)