def adicionar_apoio(self, apoio):
    self.apoios.append(apoio)  

def adicionar_carga(self, carga):
    self.cargas.append(carga)

def remover_apoio(viga, indice):
    if viga is None:
        return False
    if indice <0 or indice >= len(viga.apoios):
        return False
    viga.apoios.pop(indice)
    
    return True

def remover_carga(viga, indice):
    if viga is None:
        return False
    if indice <0 or indice >= len(viga.cargas):
        return False
    viga.cargas.pop(indice)

    return True

def listar_cargas(self):
    for c in self.cargas:
        print(type(c).__name__, vars(c))