from .Apoio import Apoio

class engaste(Apoio): # apoio fixo de grau 3, restringe momentos, Fx e Fy
    def __init__(self,posicao):
        return super().__init__(posicao)