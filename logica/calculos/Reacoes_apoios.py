def calcular_reacoes_2_apoios(self):
    modo = self.validar_estrutura()

    for apoio in self.apoios:
        apoio.reacao_y = 0.0
        apoio.reacao_x = 0.0
        apoio.momento_reacao = 0.0

    total_forcas = self.resultante_cargas()
    total_momentos = self.momento_total_origem()

    if modo == "engaste":
        apoio = self.apoios[0]
        apoio.reacao_y = total_forcas
        apoio.momento_reacao = total_momentos - total_forcas * apoio.posicao
        return {
            "tipo": "engaste",
            "Ry": apoio.reacao_y,
            "M": apoio.momento_reacao,
        }

    a1, a2 = self.apoios[0], self.apoios[1]
    distancia = a2.posicao - a1.posicao
    if abs(distancia) < 1e-9:
        raise ValueError("Os apoios não podem estar na mesma posição.")

    # Equilíbrio: R1 + R2 = total_forcas; momento na origem: R1*x1 + R2*x2 = total_momentos.
    r2 = (total_momentos - total_forcas * a1.posicao) / distancia
    r1 = total_forcas - r2

    a1.reacao_y = r1
    a2.reacao_y = r2

    return {
        "tipo": "pino_rolete",
        "apoio_1": a1,
        "apoio_2": a2,
        "R1": r1,
        "R2": r2,
    }