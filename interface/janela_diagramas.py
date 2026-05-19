import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


janela_diagramas_aberta = None
canvas_diagramas = None
fig_diagramas = None
cards_vars = {}


def _limites_y(valores):
    if not valores:
        return -1, 1

    minimo = min(valores)
    maximo = max(valores)

    if abs(maximo - minimo) < 1e-9:
        base = max(abs(maximo), 1)
        return -base * 1.2, base * 1.2

    margem = (maximo - minimo) * 0.18
    return minimo - margem, maximo + margem


def _criar_card(parent, chave, titulo, valor):
    card = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#d9e2ec",
        highlightthickness=1,
        padx=14,
        pady=10
    )
    card.pack(side="left", fill="x", expand=True, padx=6, pady=8)

    tk.Label(
        card,
        text=titulo,
        bg="white",
        fg="#52616b",
        font=("Arial", 8, "bold")
    ).pack(anchor="w")

    var = tk.StringVar(value=valor)
    cards_vars[chave] = var

    tk.Label(
        card,
        textvariable=var,
        bg="white",
        fg="#102a43",
        font=("Arial", 13, "bold")
    ).pack(anchor="w", pady=(4, 0))


def _atualizar_cards(vs, ms):
    cards_vars["vmax"].set(f"{max(vs):.2f} N")
    cards_vars["vmin"].set(f"{min(vs):.2f} N")
    cards_vars["mmax"].set(f"{max(ms):.2f} N.m")
    cards_vars["mmin"].set(f"{min(ms):.2f} N.m")


def _plotar_diagrama(ax, xs, ys, titulo, ylabel, cor):
    ax.clear()

    ax.plot(xs, ys, color=cor, linewidth=1.9)
    ax.fill_between(xs, ys, 0, color=cor, alpha=0.14)

    ax.axhline(
        0,
        color="#333333",
        linestyle="--",
        linewidth=0.9,
        alpha=0.75
    )

    ax.set_title(titulo, fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("x (m)", fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)

    ax.grid(True, linestyle="--", alpha=0.22)

    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(*_limites_y(ys))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _atualizar_graficos(xs, vs, ms):
    global fig_diagramas, canvas_diagramas

    fig_diagramas.clear()

    ax_v = fig_diagramas.add_subplot(1, 2, 1)
    ax_m = fig_diagramas.add_subplot(1, 2, 2)

    _plotar_diagrama(
        ax_v,
        xs,
        vs,
        "Diagrama de Força Cortante (V)",
        "V (N)",
        "#1f4ed8"
    )

    _plotar_diagrama(
        ax_m,
        xs,
        ms,
        "Diagrama de Momento Fletor (M)",
        "M (N.m)",
        "#15803d"
    )

    fig_diagramas.tight_layout(pad=3.0)
    canvas_diagramas.draw_idle()


def abrir_janela_diagramas(parent, viga, xs=None, vs=None, ms=None):
    global janela_diagramas_aberta
    global canvas_diagramas
    global fig_diagramas
    global cards_vars

    if xs is None or vs is None or ms is None:
        xs, vs = viga.gerar_diagrama_cortante(0.01)
        _, ms = viga.gerar_diagrama_momento(0.01)

    janela_existe = (
        janela_diagramas_aberta is not None
        and janela_diagramas_aberta.winfo_exists()
    )

    if janela_existe:
        _atualizar_cards(vs, ms)
        _atualizar_graficos(xs, vs, ms)

        janela_diagramas_aberta.lift()
        janela_diagramas_aberta.focus_force()
        return

    cards_vars = {}

    janela_diagramas_aberta = tk.Toplevel(parent)
    janela_diagramas_aberta.title("Diagramas - Força Cortante e Momento Fletor")
    janela_diagramas_aberta.geometry("1120x620")
    janela_diagramas_aberta.minsize(980, 540)
    janela_diagramas_aberta.configure(bg="#eef5f9")

    def ao_fechar():
        global janela_diagramas_aberta
        global canvas_diagramas
        global fig_diagramas
        global cards_vars

        janela_diagramas_aberta.destroy()
        janela_diagramas_aberta = None
        canvas_diagramas = None
        fig_diagramas = None
        cards_vars = {}

    janela_diagramas_aberta.protocol("WM_DELETE_WINDOW", ao_fechar)

    topo = tk.Frame(janela_diagramas_aberta, bg="#1c2b39", height=58)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Diagramas de Carregamentos Internos",
        bg="#1c2b39",
        fg="white",
        font=("Arial", 13, "bold")
    ).pack(pady=(10, 0))

    tk.Label(
        topo,
        text="Força Cortante (V) e Momento Fletor (M)",
        bg="#1c2b39",
        fg="#d9e2ec",
        font=("Arial", 9)
    ).pack()

    area_cards = tk.Frame(janela_diagramas_aberta, bg="#eef5f9")
    area_cards.pack(fill="x", padx=16, pady=(12, 4))

    _criar_card(area_cards, "vmax", "Força Cortante Máx (+)", f"{max(vs):.2f} N")
    _criar_card(area_cards, "vmin", "Força Cortante Mín (-)", f"{min(vs):.2f} N")
    _criar_card(area_cards, "mmax", "Momento Fletor Máx (+)", f"{max(ms):.2f} N.m")
    _criar_card(area_cards, "mmin", "Momento Fletor Mín (-)", f"{min(ms):.2f} N.m")

    frame_graficos = tk.Frame(
        janela_diagramas_aberta,
        bg="white",
        highlightbackground="#d9e2ec",
        highlightthickness=1
    )
    frame_graficos.pack(fill="both", expand=True, padx=18, pady=14)

    fig_diagramas = Figure(figsize=(11, 4.8), dpi=100)
    fig_diagramas.patch.set_facecolor("white")

    canvas_diagramas = FigureCanvasTkAgg(
        fig_diagramas,
        master=frame_graficos
    )

    canvas_diagramas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    _atualizar_graficos(xs, vs, ms)

    rodape = tk.Frame(janela_diagramas_aberta, bg="#eef5f9")
    rodape.pack(fill="x", padx=18, pady=(0, 12))

    ttk.Button(
        rodape,
        text="Fechar",
        command=ao_fechar
    ).pack(side="right")