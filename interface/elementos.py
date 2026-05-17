from matplotlib.patches import Polygon, Circle, FancyArrow, Rectangle, Arc


class ElementosViga:
    def __init__(self, ax, canvas, comprimento=10.0):
        self.ax = ax
        self.canvas = canvas
        self.comprimento = comprimento
        self.viga_criada = False
        self.apoios = []
        self.cargas = []
        self.reacoes = []

    def escala_visual(self):
        return max(0.25, float(self.comprimento) * 0.025)

    def limpar(self):
        self.apoios.clear()
        self.cargas.clear()
        self.reacoes.clear()
        self.atualizar()

    def adicionar_apoio(self, tipo, posicao):
        self.viga_criada = True
        self.apoios.append({"tipo": tipo, "x": float(posicao)})
        self.atualizar()

    def adicionar_carga(self, tipo, dados):
        self.viga_criada = True
        self.cargas.append({"tipo": tipo, "dados": dados})
        self.atualizar()

    def adicionar_reacao(self, posicao, valor):
        self.reacoes.append({"x": float(posicao), "valor": float(valor)})
        self.atualizar()

    def definir_reacoes(self, reacoes):
        self.reacoes = []
        for posicao, valor in reacoes:
            self.reacoes.append({"x": float(posicao), "valor": float(valor)})
        self.atualizar()

    def remover_apoio(self, indice):
        if 0 <= indice < len(self.apoios):
            del self.apoios[indice]
        self.reacoes.clear()
        self.atualizar()

    def remover_carga(self, indice):
        if 0 <= indice < len(self.cargas):
            del self.cargas[indice]
        self.reacoes.clear()
        self.atualizar()

    def configurar(self):
        self.ax.clear()
        L = max(float(self.comprimento), 1.0)
        self.ax.set_xlim(-0.08 * L, 1.08 * L)
        self.ax.set_ylim(-4.2, 4.8)
        self.ax.set_xlabel("Posição na viga (m)")
        self.ax.set_yticks([])
        self.ax.grid(True, axis="x", linestyle="--", alpha=0.30)

    def desenhar_viga(self):
        L = float(self.comprimento)
        altura = 0.34

        corpo = Rectangle(
            (0, -altura / 2),
            L,
            altura,
            facecolor="#1f77b4",
            edgecolor="none",
            alpha=0.92,
            zorder=2,
        )
        self.ax.add_patch(corpo)

        self.ax.plot([0, L], [altura / 2, altura / 2], color="black", linewidth=2, solid_capstyle="round", zorder=3)
        self.ax.plot([0, L], [-altura / 2, -altura / 2], color="black", linewidth=2, solid_capstyle="round", zorder=3)
        self.ax.plot([0, 0], [-altura / 2, altura / 2], color="black", linewidth=1, zorder=3)
        self.ax.plot([L, L], [-altura / 2, altura / 2], color="black", linewidth=1, zorder=3)

    def desenhar_pino(self, x):
        s = self.escala_visual()
        triangulo = Polygon(
            [(x - s, -1.0), (x + s, -1.0), (x, -0.18)],
            closed=True,
            facecolor="#1f77b4",
            edgecolor="black",
            linewidth=1.4,
            zorder=4,
        )
        self.ax.add_patch(triangulo)
        self.ax.plot([x - 1.25 * s, x + 1.25 * s], [-1.08, -1.08], color="black", linewidth=1.0, zorder=4)

    def desenhar_rolete(self, x):
        self.desenhar_pino(x)
        s = self.escala_visual()

        for dx in (-0.45 * s, 0.45 * s):
            roda = Circle(
                (x + dx, -1.23),
                0.20 * s,
                facecolor="lightgray",
                edgecolor="black",
                linewidth=0.8,
                zorder=5,
            )
            self.ax.add_patch(roda)

        self.ax.plot([x - 1.35 * s, x + 1.35 * s], [-1.45, -1.45], color="black", linewidth=1.0, zorder=4)

    def desenhar_engaste(self, x):
        s = self.escala_visual()
        largura = 0.28 * s
        parede = Rectangle(
            (x - largura / 2, -2.0),
            largura,
            4.0,
            facecolor="gray",
            edgecolor="black",
            linewidth=1.0,
            alpha=0.85,
            zorder=4,
        )
        self.ax.add_patch(parede)

        for i in range(9):
            y = -1.8 + i * 0.45
            self.ax.plot([x - largura / 2, x - largura / 2 - 0.35 * s], [y, y - 0.25], color="black", linewidth=0.7, zorder=4)

    def desenhar_reacao(self, x, valor):
        if abs(valor) < 1e-9:
            return

        sentido = 1 if valor >= 0 else -1
        y_inicio = -3.25 if sentido > 0 else -1.15
        dy = 1.75 * sentido

        seta = FancyArrow(
            x,
            y_inicio,
            0,
            dy,
            width=0.045,
            head_width=0.20,
            head_length=0.28,
            length_includes_head=True,
            color="red",
            zorder=6,
        )
        self.ax.add_patch(seta)
        self.ax.text(x, y_inicio - 0.35 if sentido > 0 else y_inicio + 0.55, f"{valor:.2f} N", ha="center", fontsize=8, fontweight="bold", color="red")

    def desenhar_carga_concentrada(self, x, intensidade):
        cor = "green" if intensidade >= 0 else "red"
        if intensidade >= 0:
            y_inicio, dy, y_texto = 3.8, -3.35, 4.15
        else:
            y_inicio, dy, y_texto = 0.45, 3.20, 3.95

        seta = FancyArrow(
            x,
            y_inicio,
            0,
            dy,
            width=0.045,
            head_width=0.20,
            head_length=0.30,
            length_includes_head=True,
            color=cor,
            zorder=5,
        )
        self.ax.add_patch(seta)
        self.ax.text(x, y_texto, f"P={intensidade:g}", ha="center", fontsize=8, color=cor)

    def desenhar_carga_constante(self, x1, x2, intensidade):
        if x2 <= x1:
            return

        cor = "blue"
        n = 10
        y_topo = 3.8
        y_fim = 0.35
        for i in range(n + 1):
            xi = x1 + (x2 - x1) * i / n
            seta = FancyArrow(
                xi,
                y_topo,
                0,
                y_fim - y_topo,
                width=0.03,
                head_width=0.14,
                head_length=0.24,
                length_includes_head=True,
                color=cor,
                zorder=5,
            )
            self.ax.add_patch(seta)

        self.ax.plot([x1, x2], [y_topo, y_topo], color=cor, linewidth=2.0, zorder=5)
        self.ax.text((x1 + x2) / 2, y_topo + 0.30, f"q={intensidade:g}", ha="center", fontsize=8, color=cor)

    def desenhar_carga_linear(self, x1, x2, q1, q2):
        if x2 <= x1:
            return

        cor = "purple"
        n = 10
        q_max = max(abs(q1), abs(q2), 1.0)
        pontos_x = []
        pontos_y = []

        for i in range(n + 1):
            xi = x1 + (x2 - x1) * i / n
            qi = q1 + (q2 - q1) * i / n
            comprimento_seta = 1.0 + 2.4 * abs(qi) / q_max
            y_topo = 0.35 + comprimento_seta
            pontos_x.append(xi)
            pontos_y.append(y_topo)

            if qi >= 0:
                y_inicio = y_topo
                dy = 0.35 - y_topo
            else:
                y_inicio = 0.35
                dy = y_topo - 0.35

            seta = FancyArrow(
                xi,
                y_inicio,
                0,
                dy,
                width=0.03,
                head_width=0.14,
                head_length=0.24,
                length_includes_head=True,
                color=cor,
                zorder=5,
            )
            self.ax.add_patch(seta)

        self.ax.plot(pontos_x, pontos_y, color=cor, linewidth=2.0, zorder=5)
        self.ax.text((x1 + x2) / 2, max(pontos_y) + 0.35, "q(x)", ha="center", fontsize=8, color=cor)

    def desenhar_momento(self, x, intensidade):
        cor = "orange"
        raio = 0.42
        arco = Arc((x, 1.2), 2 * raio, 2 * raio, theta1=35, theta2=315, color=cor, linewidth=2.0, zorder=5)
        self.ax.add_patch(arco)

        direcao = 1 if intensidade >= 0 else -1
        seta = FancyArrow(
            x + direcao * 0.30,
            1.48,
            direcao * 0.12,
            -0.05,
            width=0.025,
            head_width=0.16,
            head_length=0.15,
            color=cor,
            zorder=5,
        )
        self.ax.add_patch(seta)
        self.ax.text(x, 1.85, f"M={intensidade:g}", ha="center", fontsize=8, color=cor)

    def _iterar_apoios(self):
        for apoio in self.apoios:
            if isinstance(apoio, dict):
                yield apoio.get("tipo", ""), float(apoio.get("x", 0.0))
            else:
                yield apoio[0], float(apoio[1])

    def _iterar_cargas(self):
        for carga in self.cargas:
            if isinstance(carga, dict):
                yield carga.get("tipo", ""), carga.get("dados", {})
            else:
                yield carga[0], carga[1]

    def _iterar_reacoes(self):
        for reacao in self.reacoes:
            if isinstance(reacao, dict):
                yield float(reacao.get("x", 0.0)), float(reacao.get("valor", 0.0))
            else:
                yield float(reacao[0]), float(reacao[1])

    def atualizar(self):
        self.configurar()

        if not self.viga_criada:
            self.ax.text(0.5, 0.5, "Crie uma viga para iniciar", ha="center", va="center", transform=self.ax.transAxes)
            self.canvas.draw_idle()
            return

        self.desenhar_viga()

        for tipo, posicao in self._iterar_apoios():
            tipo_normalizado = str(tipo).lower()
            if "pino" in tipo_normalizado:
                self.desenhar_pino(posicao)
            elif "rolete" in tipo_normalizado:
                self.desenhar_rolete(posicao)
            elif "engast" in tipo_normalizado:
                self.desenhar_engaste(posicao)

        for posicao, valor in self._iterar_reacoes():
            self.desenhar_reacao(posicao, valor)

        for tipo, dados in self._iterar_cargas():
            if tipo == "concentrada":
                self.desenhar_carga_concentrada(dados["x"], dados["valor"])
            elif tipo == "constante":
                self.desenhar_carga_constante(dados["x1"], dados["x2"], dados["valor"])
            elif tipo == "linear":
                self.desenhar_carga_linear(dados["x1"], dados["x2"], dados["q1"], dados["q2"])
            elif tipo == "momento":
                self.desenhar_momento(dados["x"], dados["valor"])

        self.canvas.draw_idle()