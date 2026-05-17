class Momento_Binario:
    def __init__(self, intensidade, posicao):
        self.intensidade = float(intensidade)
        self.posicao = float(posicao)

    def resultante(self):
        return 0.0

    def momento_origem(self):
        return self.intensidade

    def resultante_ate(self, x, passo=0.01):
        return 0.0

    def momento_ate(self, x, passo=0.01):
        return self.intensidade if self.posicao <= x else 0.0

    def __str__(self):
        return f"Momento: M={self.intensidade:g} em x={self.posicao:g}"