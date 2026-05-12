import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.patches import Polygon
from matplotlib.patches import Circle
from matplotlib.patches import FancyArrow

class ElementosViga:

    def __init__(self, frame, comprimento=10):

        self.comprimento = comprimento

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

        self.atualizar()

    # CONFIGURAÇÃO
    def configurar(self):

        self.ax.clear()

        self.ax.set_xlim(-1, self.comprimento + 1)

        self.ax.set_ylim(-3, 3)

        self.ax.axhline(
            0,
            color='black',
            linewidth=4
        )

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

        self.ax.plot(
            [0, self.comprimento],
            [0, 0],
            linewidth=8,
            color='black'
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

        self.apoios.append(
            (tipo, posicao)
        )

        self.atualizar()

    # ADICIONAR REAÇÃO
    def adicionar_reacao(self, posicao, valor):
        self.reacoes.append(
            (posicao, valor)
        )

        self.atualizar()

    # ATUALIZAÇÃO
    def atualizar(self):

        self.configurar()

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

        self.canvas.draw()