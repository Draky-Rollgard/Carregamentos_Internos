from logica.Viga import Viga
from logica.apoios import pino, rolete
from logica.carregamentos import Carregamento_Concentrado

v = Viga(10)
v.adicionar_apoio(pino(0))
v.adicionar_apoio(rolete(10))
v.adicionar_carga(Carregamento_Concentrado(100, 5))
print(v.calcular_reacoes_2_apoios())
print(v.forca_cortante_em(4), v.momento_fletor_em(5))