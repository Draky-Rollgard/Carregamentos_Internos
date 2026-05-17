from .Distribuido import Distribuido

class Linear(Distribuido):
    def __init__(self, intensidade_inicial, intensidade_final, posicao_inicial, posicao_final):
        self.intensidade_inicial = float(intensidade_inicial)
        self.intensidade_final = float(intensidade_final)
        super().__init__(posicao_inicial, posicao_final)

    def intensidade_em(self, x):
        L = self.posicao_final - self.posicao_inicial
        t = (float(x) - self.posicao_inicial) / L
        return self.intensidade_inicial + (self.intensidade_final - self.intensidade_inicial) * t

    def __str__(self):
        return (
            f"Linear: q1={self.intensidade_inicial:g}, q2={self.intensidade_final:g}, "
            f"x={self.posicao_inicial:g} a {self.posicao_final:g}"
        )