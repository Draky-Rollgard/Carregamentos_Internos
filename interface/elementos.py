from matplotlib.patches import Rectangle


class ElementosViga:
    def __init__(self, ax, canvas, comprimento=10.0):
        self.ax = ax
        self.canvas = canvas
        self.comprimento = comprimento
        self.viga_criada = False
        self.apoios = []
        self.cargas = []
        self.reacoes = []

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
            self.reacoes.append(
                {
                    "x": float(posicao),
                    "valor": float(valor)
                }
            )

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
        margem = max(0.08 * L, 2.0)

        self.ax.set_xlim(-margem, L + margem)
        self.ax.set_ylim(-3.7, 4.6)

        self.ax.set_xlabel("Posição na viga (m)")
        self.ax.set_yticks([])

        self.ax.grid(
            True,
            axis="x",
            linestyle="--",
            alpha=0.25
        )

    def desenhar_viga(self):
        L = float(self.comprimento)
        altura = 0.34

        corpo = Rectangle(
            (0, -altura / 2),
            L,
            altura,
            facecolor="#1f77b4",
            edgecolor="none",
            alpha=0.90,
            zorder=2
        )

        self.ax.add_patch(corpo)

        self.ax.plot(
            [0, L],
            [altura / 2, altura / 2],
            color="black",
            linewidth=2,
            solid_capstyle="round",
            zorder=3
        )

        self.ax.plot(
            [0, L],
            [-altura / 2, -altura / 2],
            color="black",
            linewidth=2,
            solid_capstyle="round",
            zorder=3
        )

        self.ax.plot(
            [0, 0],
            [-altura / 2, altura / 2],
            color="black",
            linewidth=1,
            zorder=3
        )

        self.ax.plot(
            [L, L],
            [-altura / 2, altura / 2],
            color="black",
            linewidth=1,
            zorder=3
        )

    # =========================
    # APOIOS COM TAMANHO FIXO
    # =========================

    def desenhar_pino(self, x):
        # Triângulo com tamanho visual fixo e próximo da viga
        self.ax.scatter(
            [x],
            [-0.5],
            marker="^",
            s=400,
            facecolors="#1f77b4",
            edgecolors="black",
            linewidths=1.4,
            zorder=4
        )

        # Base do pino
        self.ax.scatter(
            [x],
            [-0.9],
            marker="_",
            s=950,
            c="black",
            linewidths=1.1,
            zorder=4
        )

    def desenhar_rolete(self, x):
        # Rolete: apenas um círculo, um pouco maior
        self.ax.scatter(
            [x],
            [-0.5],
            marker="o",
            s=400,
            facecolors="lightgray",
            edgecolors="black",
            linewidths=1.0,
            zorder=5
        )

        # Base inferior do rolete
        self.ax.scatter(
            [x],
            [-0.9],
            marker="_",
            s=850,
            c="black",
            linewidths=1.1,
            zorder=4
        )
    def desenhar_engaste(self, x):
        self.ax.plot(
            [x, x],
            [-2.0, 2.0],
            linewidth=10,
            color="gray",
            zorder=4
        )

        for y in [-1.7, -1.2, -0.7, -0.2, 0.3, 0.8, 1.3, 1.8]:
            self.ax.plot(
                [x, x - 0.9],
                [y, y - 0.22],
                color="black",
                linewidth=0.7,
                zorder=4
            )

    def desenhar_reacao(self, x, valor):
        if abs(valor) < 1e-9:
            return

        if valor >= 0:
            self.ax.annotate(
                "",
                xy=(x, -0.95),
                xytext=(x, -2.65),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="red",
                    lw=1.6,
                    mutation_scale=16,
                    shrinkA=0,
                    shrinkB=0
                ),
                zorder=6
            )

            y_texto = -3.00

        else:
            self.ax.annotate(
                "",
                xy=(x, -2.65),
                xytext=(x, -0.95),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="red",
                    lw=1.6,
                    mutation_scale=16,
                    shrinkA=0,
                    shrinkB=0
                ),
                zorder=6
            )

            y_texto = -0.70

        self.ax.text(
            x,
            y_texto,
            f"{valor:.2f} N",
            ha="center",
            fontsize=8,
            fontweight="bold",
            color="red"
        )

    def desenhar_carga_concentrada(self, x, intensidade):
        cor = "green" if intensidade >= 0 else "red"

        if intensidade >= 0:
            self.ax.annotate(
                "",
                xy=(x, 0.35),
                xytext=(x, 3.60),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor,
                    lw=1.6,
                    mutation_scale=16,
                    shrinkA=0,
                    shrinkB=0
                ),
                zorder=5
            )

            y_texto = 3.95

        else:
            self.ax.annotate(
                "",
                xy=(x, 3.60),
                xytext=(x, 0.35),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor,
                    lw=1.6,
                    mutation_scale=16,
                    shrinkA=0,
                    shrinkB=0
                ),
                zorder=5
            )

            y_texto = 3.95

        self.ax.text(
            x,
            y_texto,
            f"P={intensidade:g}",
            ha="center",
            fontsize=8,
            color=cor
        )

    def desenhar_carga_constante(self, x1, x2, intensidade):
        if x2 <= x1:
            return

        cor = "blue"
        y_topo = 3.60
        y_base = 0.35
        n = 10

        self.ax.plot(
            [x1, x2],
            [y_topo, y_topo],
            color=cor,
            linewidth=2.0,
            zorder=5
        )

        for i in range(n + 1):
            xi = x1 + (x2 - x1) * i / n

            self.ax.annotate(
                "",
                xy=(xi, y_base),
                xytext=(xi, y_topo),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor,
                    lw=1.1,
                    mutation_scale=12,
                    shrinkA=0,
                    shrinkB=0
                ),
                zorder=5
            )

        self.ax.text(
            (x1 + x2) / 2,
            y_topo + 0.30,
            f"q={intensidade:g}",
            ha="center",
            fontsize=8,
            color=cor
        )

    def desenhar_carga_linear(self, x1, x2, q1, q2):
        if x2 <= x1:
            return

        cor = "purple"
        n = 10
        q_max = max(abs(q1), abs(q2), 1.0)

        xs = []
        ys = []

        for i in range(n + 1):
            xi = x1 + (x2 - x1) * i / n
            qi = q1 + (q2 - q1) * i / n

            altura = 1.0 + 2.4 * abs(qi) / q_max
            y_topo = 0.35 + altura

            xs.append(xi)
            ys.append(y_topo)

            if qi >= 0:
                self.ax.annotate(
                    "",
                    xy=(xi, 0.35),
                    xytext=(xi, y_topo),
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color=cor,
                        lw=1.1,
                        mutation_scale=12,
                        shrinkA=0,
                        shrinkB=0
                    ),
                    zorder=5
                )

            else:
                self.ax.annotate(
                    "",
                    xy=(xi, y_topo),
                    xytext=(xi, 0.35),
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color=cor,
                        lw=1.1,
                        mutation_scale=12,
                        shrinkA=0,
                        shrinkB=0
                    ),
                    zorder=5
                )

        self.ax.plot(
            xs,
            ys,
            color=cor,
            linewidth=2.0,
            zorder=5
        )

        self.ax.text(
            (x1 + x2) / 2,
            max(ys) + 0.35,
            "q(x)",
            ha="center",
            fontsize=8,
            color=cor
        )

    def desenhar_momento(self, x, intensidade):
        cor = "orange"

        if intensidade >= 0:
            self.ax.annotate(
                "",
                xy=(x + 0.55, 1.15),
                xytext=(x - 0.55, 1.15),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor,
                    lw=1.8,
                    mutation_scale=16,
                    connectionstyle="arc3,rad=1.2"
                ),
                zorder=5
            )

        else:
            self.ax.annotate(
                "",
                xy=(x - 0.55, 1.15),
                xytext=(x + 0.55, 1.15),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor,
                    lw=1.8,
                    mutation_scale=16,
                    connectionstyle="arc3,rad=1.2"
                ),
                zorder=5
            )

        self.ax.text(
            x,
            1.90,
            f"M={intensidade:g}",
            ha="center",
            fontsize=8,
            color=cor
        )

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
            self.ax.text(
                0.5,
                0.5,
                "Crie uma viga para iniciar",
                ha="center",
                va="center",
                transform=self.ax.transAxes
            )
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
                self.desenhar_carga_concentrada(
                    dados["x"],
                    dados["valor"]
                )

            elif tipo == "constante":
                self.desenhar_carga_constante(
                    dados["x1"],
                    dados["x2"],
                    dados["valor"]
                )

            elif tipo == "linear":
                self.desenhar_carga_linear(
                    dados["x1"],
                    dados["x2"],
                    dados["q1"],
                    dados["q2"]
                )

            elif tipo == "momento":
                self.desenhar_momento(
                    dados["x"],
                    dados["valor"]
                )

        self.canvas.draw_idle()