def resultante_cargas(self):
    total = 0.0
    for carga in self.cargas:
        if hasattr(carga, "resultante"):
            total += carga.resultante()
    return total