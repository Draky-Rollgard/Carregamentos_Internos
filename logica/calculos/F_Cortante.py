def forca_cortante_em(self, x):
    x = float(x)
    V = 0.0

    for apoio in self.apoios:
        if apoio.posicao <= x + 1e-9:
            V += apoio.reacao_y

    for carga in self.cargas:
        if hasattr(carga, "resultante_ate"):
            V -= carga.resultante_ate(x)

    return V

def gerar_diagrama_cortante(self, passo=0.01):
    xs = self.gerar_pontos_x(passo)
    vs = [self.forca_cortante_em(x) for x in xs]
    return xs, vs