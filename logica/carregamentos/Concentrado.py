class Carregamento_Concentrado:
    def __init__(self, intensidade, posicao):
        self.intensidade = float(intensidade)
        self.posicao = float(posicao)

    def resultante(self):
        return self.intensidade

    def centroide(self):
        return self.posicao

    def resultante_ate(self, x, passo=0.01):
        return self.intensidade if self.posicao <= x else 0.0

    def momento_ate(self, x, passo=0.01):
        return self.intensidade * (x - self.posicao) if self.posicao <= x else 0.0

    def momento_origem(self):
        return self.intensidade * self.posicao

    def __str__(self):
        return f"Concentrado: P={self.intensidade:g} em x={self.posicao:g}"