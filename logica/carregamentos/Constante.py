from .Distribuido import Distribuido

class Constante(Distribuido):
    def __init__(self, intensidade, posicao_inicial, posicao_final):
        self.intensidade = float(intensidade)
        super().__init__(posicao_inicial, posicao_final)

    def intensidade_em(self, x):
        return self.intensidade

    def resultante(self, passo=0.01):
        return self.intensidade * (self.posicao_final - self.posicao_inicial)

    def momento_origem(self, passo=0.01):
        return self.resultante() * self.centroide()

    def centroide(self, passo=0.01):
        return (self.posicao_inicial + self.posicao_final) / 2.0

    def __str__(self):
        return f"Constante: q={self.intensidade:g}, x={self.posicao_inicial:g} a {self.posicao_final:g}"