from .apoios import *
from .operacoes import *
from .calculos import *
from .carregamentos import *
from .Viga import Viga

'''
Problema:

Viga biapoiada de 10 m.

Apoio pino em x=0
Apoio rolete em x=10
Carga de 100 N em x=5

Resultado teórico:

Ay = 50
By = 50
'''

v1 = Viga(10)

v1.adicionar_apoio(pino(0))
v1.adicionar_apoio(rolete(10))

v1.adicionar_carga(Carregamento_Concentrado(100,5))

v1.listar_cargas()
print(v1.calcular_reacoes_2_apoios())