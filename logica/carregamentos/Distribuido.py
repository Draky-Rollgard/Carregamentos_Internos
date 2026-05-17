class Distribuido:
    def __init__(self, posicao_inicial, posicao_final):
        self.posicao_inicial = float(posicao_inicial)
        self.posicao_final = float(posicao_final)
        if self.posicao_final <= self.posicao_inicial:
            raise ValueError("A posição final deve ser maior que a inicial.")

    def intensidade_em(self, x):
        raise NotImplementedError

    def _integrar(self, funcao, a, b, passo=0.01):
        if b <= a:
            return 0.0
        soma = 0.0
        atual = a
        while atual < b:
            prox = min(atual + passo, b)
            meio = (atual + prox) / 2.0
            soma += funcao(meio) * (prox - atual)
            atual = prox
        return soma

    def resultante(self, passo=0.01):
        return self._integrar(self.intensidade_em, self.posicao_inicial, self.posicao_final, passo)

    def momento_origem(self, passo=0.01):
        return self._integrar(lambda x: self.intensidade_em(x) * x, self.posicao_inicial, self.posicao_final, passo)

    def centroide(self, passo=0.01):
        r = self.resultante(passo)
        if abs(r) < 1e-12:
            return (self.posicao_inicial + self.posicao_final) / 2.0
        return self.momento_origem(passo) / r

    def resultante_ate(self, x, passo=0.01):
        fim = min(float(x), self.posicao_final)
        if fim <= self.posicao_inicial:
            return 0.0
        return self._integrar(self.intensidade_em, self.posicao_inicial, fim, passo)

    def momento_ate(self, x, passo=0.01):
        fim = min(float(x), self.posicao_final)
        if fim <= self.posicao_inicial:
            return 0.0
        return self._integrar(lambda s: self.intensidade_em(s) * (x - s), self.posicao_inicial, fim, passo)