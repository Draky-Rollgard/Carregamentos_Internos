def momento_total_origem(self):
    total = 0.0
    for carga in self.cargas:
        if hasattr(carga, "momento_origem"):
            total += carga.momento_origem()
    return total