def _nome_tipo(obj):
    return obj.__class__.__name__.lower()

def adicionar_apoio(self, apoio):
    if not self.validar_posicao(apoio.posicao):
        raise ValueError("Apoio fora da viga.")

    novo_tipo = _nome_tipo(apoio)
    tipos = [_nome_tipo(a) for a in self.apoios]

    for existente in self.apoios:
        if abs(existente.posicao - apoio.posicao) < 1e-9:
            raise ValueError("Já existe um apoio nessa posição.")

    if "engaste" in tipos:
        raise ValueError("Engaste deve ser utilizado sozinho.")

    if novo_tipo == "engaste" and len(self.apoios) > 0:
        raise ValueError("Engaste não pode ser combinado com pino ou rolete.")

    if novo_tipo in ("pino", "rolete"):
        if novo_tipo in tipos:
            raise ValueError(f"Já existe um apoio do tipo {novo_tipo}.")
        if len(self.apoios) >= 2:
            raise ValueError("Use apenas um pino e um rolete.")

    self.apoios.append(apoio)
    return True

def adicionar_carga(self, carga):
    self.validar_carga(carga)
    self.cargas.append(carga)
    return True

def remover_apoio(viga, indice):
    if viga is None:
        return False
    if 0 <= indice < len(viga.apoios):
        del viga.apoios[indice]
        return True
    return False

def remover_carga(viga, indice):
    if viga is None:
        return False
    if 0 <= indice < len(viga.cargas):
        del viga.cargas[indice]
        return True
    return False

def listar_cargas(self):
    return [str(carga) for carga in self.cargas]