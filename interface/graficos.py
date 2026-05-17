def plotar_diagramas(fig, canvas, viga):
    fig.clear()
    ax_v = fig.add_subplot(1, 2, 1)
    ax_m = fig.add_subplot(1, 2, 2)

    xs, vs = viga.gerar_diagrama_cortante(0.01)
    _, ms = viga.gerar_diagrama_momento(0.01)

    ax_v.plot(xs, vs, linewidth=1.3)
    ax_v.fill_between(xs, vs, 0, alpha=0.15)
    ax_v.axhline(0, linestyle="--", linewidth=0.8)
    ax_v.set_title("Diagrama de Força Cortante (V)", fontsize=9)
    ax_v.set_xlabel("x (m)")
    ax_v.set_ylabel("V (N)")
    ax_v.grid(True, alpha=0.25)

    ax_m.plot(xs, ms, linewidth=1.3)
    ax_m.fill_between(xs, ms, 0, alpha=0.15)
    ax_m.axhline(0, linestyle="--", linewidth=0.8)
    ax_m.set_title("Diagrama de Momento Fletor (M)", fontsize=9)
    ax_m.set_xlabel("x (m)")
    ax_m.set_ylabel("M (N.m)")
    ax_m.grid(True, alpha=0.25)

    fig.tight_layout()
    canvas.draw_idle()
    return xs, vs, ms