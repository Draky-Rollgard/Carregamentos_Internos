class Apoio:
    def __init__(self, posicao):
        self.posicao = float(posicao)
        self.reacao_y = 0.0
        self.reacao_x = 0.0
        self.momento_reacao = 0.0

    @property
    def tipo(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return f"{self.tipo} em x={self.posicao:g}"