def momento_fletor_em(self, x):
    x = float(x)
    M = 0.0

    for apoio in self.apoios:
        if apoio.posicao <= x + 1e-9:
            M += apoio.reacao_y * (x - apoio.posicao)
            if apoio.__class__.__name__.lower() == "engaste":
                M -= apoio.momento_reacao

    for carga in self.cargas:
        if hasattr(carga, "momento_ate"):
            M -= carga.momento_ate(x)

    return M

def gerar_diagrama_momento(self, passo=0.01):
    xs = self.gerar_pontos_x(passo)
    ms = [self.momento_fletor_em(x) for x in xs]
    return xs, ms