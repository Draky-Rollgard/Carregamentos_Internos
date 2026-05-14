import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.patches import Polygon
from matplotlib.patches import Circle
from matplotlib.patches import FancyArrow
from matplotlib.patches import Rectangle

class ElementosViga:

    def __init__(self, frame, comprimento=10):

        self.comprimento = comprimento
        self.cargas = []

        self.fig = Figure(figsize=(8, 3), dpi=100)

        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.apoios = []
        self.reacoes = []
        self.viga_criada = False

        self.atualizar()

    # CONFIGURAÇÃO
    def configurar(self):

        self.ax.clear()

        self.ax.set_xlim(-1, self.comprimento + 1)

        self.ax.set_ylim(-3, 3)

        self.ax.set_yticks([])

        self.ax.grid(
            True,
            linestyle='--',
            alpha=0.3
        )

        self.ax.set_xlabel(
            "Posição na viga (m)"
        )

    # VIGA
    def desenhar_viga(self):

        altura_total = 0.28
        altura_centro = 0.16

        y_base = -altura_total / 2

        # Corpo central azul
        corpo = Rectangle(
            (0, -altura_centro / 2),
            self.comprimento,
            altura_centro,
            facecolor='#1f77b4',
            edgecolor='none',
            zorder=2
        )

        self.ax.add_patch(corpo)
        # ====== LINHAS =========
        # superior
        self.ax.plot(
            [0, self.comprimento],
            [altura_total / 2, altura_total / 2],
            color='black',
            linewidth=4,
            solid_capstyle='round',
            zorder=3
        )

        # inferior
        self.ax.plot(
            [0, self.comprimento],
            [-altura_total / 2, -altura_total / 2],
            color='black',
            linewidth=4,
            solid_capstyle='round',
            zorder=3
        )

        # Laterais da viga
        self.ax.plot(
            [0, 0],
            [-altura_total / 2, altura_total / 2],
            color='black',
            linewidth=1,
            zorder=3
        )

        self.ax.plot(
            [self.comprimento, self.comprimento],
            [-altura_total / 2, altura_total / 2],
            color='black',
            linewidth=1,
            zorder=3
        )

    # PINO
    def desenhar_pino(self, x):

        triangulo = Polygon(
            [
                (x - 0.4, -0.8),
                (x + 0.4, -0.8),
                (x, 0)
            ],
            closed=True,
            color='#1f77b4'
        )

        self.ax.add_patch(triangulo)

    # ROLETE
    def desenhar_rolete(self, x):

        self.desenhar_pino(x)

        roda1 = Circle(
            (x - 0.15, -1.0),
            0.1,
            color='gray'
        )

        roda2 = Circle(
            (x + 0.15, -1.0),
            0.1,
            color='gray'
        )

        self.ax.add_patch(roda1)
        self.ax.add_patch(roda2)

    # ENGASTE
    def desenhar_engaste(self, x):

        self.ax.plot(
            [x, x],
            [-2, 2],
            linewidth=10,
            color='black'
        )

    # REAÇÃO
    def desenhar_reacao(self, x, valor):

        seta = FancyArrow(
            x,
            -2,
            0,
            1.2,
            width=0.08,
            color='red'
        )

        self.ax.add_patch(seta)

        self.ax.text(
            x,
            -2.4,
            f"{valor:.2f} N",
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='red'
        )

    # ADICIONAR APOIO
    def adicionar_apoio(self, tipo, posicao):
    
        self.viga_criada = True
        
        self.apoios.append(
            (tipo, posicao)
        )

        self.atualizar()

    def desenhar_carga_concentrada(self, x, intensidade):

        cor = 'green' if intensidade > 0 else 'red'
        altura = 1.5 if intensidade > 0 else -1.5

        seta = FancyArrow(
            x,
            altura,
            0,
            -altura,
            width=0.05,
            color=cor
        )

        self.ax.add_patch(seta)

        self.ax.text(
            x,
            altura + 0.3,
            f"{intensidade}",
            ha='center',
            fontsize=9,
            color=cor
        )
    

    def desenhar_carga_constante(self, x1, x2, intensidade):

        passo = (x2 - x1) / 10

        for i in range(11):

            xi = x1 + i * passo

            seta = FancyArrow(
                xi,
                2,
                0,
                -1.2,
                width=0.03,
                color='blue'
            )

            self.ax.add_patch(seta)

        self.ax.plot(
            [x1, x2],
            [2.2, 2.2], 
            color='blue',
            linewidth=2
        )

        self.ax.text(
            (x1 + x2) / 2,
            2.5,
            f"q={intensidade}",
            ha='center',
            color='blue'
        )

    def desenhar_carga_linear(self, x1, x2, q1, q2):

        passos = 10

        for i in range(passos + 1):

            xi = x1 + (x2 - x1) * i / passos
            qi = q1 + (q2 - q1) * i / passos

            altura = 2 + qi * 0.5

            seta = FancyArrow(
                xi,
                2,
                0,
                altura - 2,
                width=0.03,
                color='purple'
            )

            self.ax.add_patch(seta)

        self.ax.text(
            (x1 + x2) / 2,
            2.8,
            f"q(x)",
            ha='center',
            color='purple'
        )

    def desenhar_momento(self, x, intensidade):

        arco = FancyArrow(
            x,
            1.5,
            0.5,
            0,
            width=0.02,
            color='orange'
        )

        self.ax.add_patch(arco)

        self.ax.text(
            x,
            1.8,
            f"M={intensidade}",
            ha='center',
            color='orange'
        )
    


    # ADICIONAR REAÇÃO
    def adicionar_reacao(self, posicao, valor):
        self.reacoes.append(
            (posicao, valor)
        )

        self.atualizar()
    
    # ADICIONAR CARGA
    def adicionar_carga(self, tipo, dados):
        self.viga_criada = True
        self.cargas.append((tipo, dados))

        self.atualizar()

    # ATUALIZAÇÃO
    def atualizar(self):

        self.configurar()

        if self.viga_criada:
            self.desenhar_viga()

        for tipo, posicao in self.apoios:

            if tipo == "Pino":
                self.desenhar_pino(posicao)

            elif tipo == "Rolete":
                self.desenhar_rolete(posicao)

            elif tipo == "Engastado":
                self.desenhar_engaste(posicao)

        for posicao, valor in self.reacoes:

            self.desenhar_reacao(
                posicao,
                valor
            )
        
        for carga in self.cargas:

            tipo = carga[0]
            d = carga[1]

            if tipo == "concentrada":
                self.desenhar_carga_concentrada(d["x"], d["valor"])

            elif tipo == "constante":
                self.desenhar_carga_constante(d["x1"], d["x2"], d["valor"])

            elif tipo == "linear":
                self.desenhar_carga_linear(d["x1"], d["x2"], d["q1"], d["q2"])

            elif tipo == "momento":
                self.desenhar_momento(d["x"], d["valor"])

        self.canvas.draw()