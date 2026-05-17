import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from logica.Viga import Viga
from logica.apoios import pino, rolete, engaste
from logica.carregamentos import Carregamento_Concentrado, Constante, Linear, Momento_Binario
from logica.operacoes.acoes import remover_apoio, remover_carga
from .elementos import ElementosViga
from .graficos import plotar_diagramas

screen = None
viga = None
elementos_viga = None

def iniciar():
    global screen, viga, elementos_viga

    screen = tk.Tk()
    screen.title("Projeto_Carregamentos_Internos")
    #screen.geometry("1080x700")
    screen.state('zoomed')
    screen.configure(bg="lightblue")

    menu_principal = tk.Menu(screen)
    screen.config(menu=menu_principal)
    menu_arq = tk.Menu(menu_principal, tearoff=0)
    menu_arq.add_command(label="Novo", command=lambda: novo_projeto())
    menu_arq.add_separator()
    menu_arq.add_command(label="Sair", command=screen.quit)
    menu_principal.add_cascade(label="Arquivo", menu=menu_arq)
    menu_principal.add_cascade(label="Editar", menu=tk.Menu(menu_principal, tearoff=0))

    topo = tk.Frame(screen, bg="#1c2b39", height=55)
    topo.pack(fill="x")
    tk.Label(
        topo,
        text="Mecânica Geral\nEstática - Carregamentos internos",
        fg="white",
        bg="#1c2b39",
        font=("Arial", 10, "bold"),
    ).pack(pady=10)

    lateral_esquerda = tk.Frame(screen, bg="#f4f4f4", width=170)
    lateral_esquerda.pack(side="left", fill="y")

    lateral_direita = tk.Frame(screen, bg="#f4f4f4", width=180)
    lateral_direita.pack(side="right", fill="y")

    centro = tk.Frame(screen, bg="lightblue")
    centro.pack(side="left", fill="both", expand=True, padx=12, pady=12)

    # =============================== GEOMETRIA ===============================
    tk.Label(lateral_esquerda, text="GEOMETRIA", font=("Arial", 8, "bold"), bg="#f4f4f4").pack(anchor="w", pady=10, padx=12)
    tk.Label(lateral_esquerda, text="Comprimento da viga", bg="#f4f4f4").pack(anchor="w", padx=12)
    entry_comprimento = tk.Entry(lateral_esquerda, width=18)
    entry_comprimento.pack(anchor="w", padx=12, pady=5)
    tk.Label(lateral_esquerda, text="Referencial", bg="#f4f4f4").pack(anchor="w", padx=12)
    entry_referencial = tk.Entry(lateral_esquerda, width=18)
    entry_referencial.pack(anchor="w", padx=12, pady=5)

    # =============================== CENTRO: VIGA ============================
    frame_viga = tk.LabelFrame(centro, text="VIGA, APOIOS E REAÇÕES", font=("Arial", 8, "bold"), bg="white")
    frame_viga.pack(fill="both", expand=True, pady=(0, 8))
    fig_viga = Figure(figsize=(7.2, 3.3), dpi=100)
    ax_viga = fig_viga.add_subplot(111)
    canvas_viga = FigureCanvasTkAgg(fig_viga, master=frame_viga)
    canvas_viga.get_tk_widget().pack(fill="both", expand=True)
    elementos_viga = ElementosViga(ax_viga, canvas_viga, 10)
    elementos_viga.atualizar()

    frame_diagramas = tk.LabelFrame(centro, text="DIAGRAMAS", font=("Arial", 8, "bold"), bg="white")
    frame_diagramas.pack(fill="both", expand=True, pady=(0, 8))
    fig_diagramas = Figure(figsize=(7.2, 2.2), dpi=100)
    ax_placeholder = fig_diagramas.add_subplot(111)
    ax_placeholder.axis("off")
    ax_placeholder.text(0.5, 0.5, "Área dos diagramas de Força Cortante e Momento Fletor", ha="center", va="center", fontsize=8)
    canvas_diagramas = FigureCanvasTkAgg(fig_diagramas, master=frame_diagramas)
    canvas_diagramas.get_tk_widget().pack(fill="both", expand=True)

    frame_resultados = tk.LabelFrame(centro, text="RESULTADOS", font=("Arial", 8, "bold"), bg="white")
    frame_resultados.pack(fill="x")
    resultados_var = tk.StringVar(value="Área para reações, cortante e momento")
    label_resultados = tk.Label(frame_resultados, textvariable=resultados_var, bg="white", justify="left", anchor="w", font=("Arial", 9))
    label_resultados.pack(fill="x", padx=14, pady=16)

    # =============================== FUNÇÕES =================================
    def limpar_listas_visuais():
        lista_apoios.delete(0, tk.END)
        lista_cargas.delete(0, tk.END)
        resultados_var.set("Área para reações, cortante e momento")
        fig_diagramas.clear()
        ax = fig_diagramas.add_subplot(111)
        ax.axis("off")
        ax.text(0.5, 0.5, "Área dos diagramas de Força Cortante e Momento Fletor", ha="center", va="center", fontsize=8)
        canvas_diagramas.draw_idle()

    def criar_viga():
        global viga
        try:
            comprimento = float(entry_comprimento.get().replace(",", "."))
            referencial = float(entry_referencial.get().replace(",", ".") or 0)
            viga = Viga(comprimento, referencial)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro) if str(erro) else "Digite um comprimento válido e maior que zero.")
            return

        elementos_viga.comprimento = comprimento
        elementos_viga.viga_criada = True
        elementos_viga.limpar()
        limpar_listas_visuais()
        resultados_var.set(f"Viga criada: L = {comprimento:g} m | Referencial = {referencial:g} m")

    def novo_projeto():
        global viga
        viga = None
        entry_comprimento.delete(0, tk.END)
        entry_referencial.delete(0, tk.END)
        entry_pos.delete(0, tk.END)
        elementos_viga.viga_criada = False
        elementos_viga.limpar()
        limpar_listas_visuais()

    def adicionar_apoio_interface():
        global viga
        if viga is None:
            messagebox.showerror("Erro", "Crie a viga antes de adicionar apoios.")
            return
        try:
            pos = float(entry_pos.get().replace(",", "."))
            tipo = combo_apoio.get()
            if tipo == "pino":
                apoio = pino(pos)
                texto_tipo = "Pino"
            elif tipo == "rolete":
                apoio = rolete(pos)
                texto_tipo = "Rolete"
            else:
                apoio = engaste(pos)
                texto_tipo = "Engastado"
            viga.adicionar_apoio(apoio)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            return

        elementos_viga.adicionar_apoio(texto_tipo, pos)
        lista_apoios.insert(tk.END, f"{tipo} em x={pos:g}")
        entry_pos.delete(0, tk.END)

    def remover_apoio_interface():
        global viga
        selecionado = lista_apoios.curselection()
        if not selecionado or viga is None:
            return
        indice = selecionado[0]
        if remover_apoio(viga, indice):
            lista_apoios.delete(indice)
            elementos_viga.remover_apoio(indice)

    def atualizar_parametros(event=None):
        for widget in frame_parametros.winfo_children():
            widget.destroy()
        campos.clear()
        tipo = combo_carregamento.get()

        def campo(nome, rotulo):
            tk.Label(frame_parametros, text=rotulo, bg="#f4f4f4").pack(anchor="w")
            entrada = tk.Entry(frame_parametros, width=22)
            entrada.pack(anchor="w", pady=4)
            campos[nome] = entrada

        if tipo == "Concentrado":
            campo("intensidade", "Intensidade")
            campo("posicao", "Posição")
        elif tipo == "Distribuído Constante":
            campo("intensidade", "Intensidade")
            campo("inicio", "Posição inicial")
            campo("fim", "Posição final")
        elif tipo == "Distribuído Linear":
            campo("q1", "Intensidade inicial")
            campo("inicio", "Posição inicial")
            campo("q2", "Intensidade final")
            campo("fim", "Posição final")
        else:
            campo("intensidade", "Intensidade do momento")
            campo("posicao", "Posição")

    def valor(nome):
        return float(campos[nome].get().replace(",", "."))

    def adicionar_carregamento_interface():
        global viga
        if viga is None:
            messagebox.showerror("Erro", "Crie a viga antes de adicionar carregamentos.")
            return
        try:
            tipo = combo_carregamento.get()
            if tipo == "Concentrado":
                carga = Carregamento_Concentrado(valor("intensidade"), valor("posicao"))
                dados = {"x": carga.posicao, "valor": carga.intensidade}
                tipo_desenho = "concentrada"
            elif tipo == "Distribuído Constante":
                carga = Constante(valor("intensidade"), valor("inicio"), valor("fim"))
                dados = {"x1": carga.posicao_inicial, "x2": carga.posicao_final, "valor": carga.intensidade}
                tipo_desenho = "constante"
            elif tipo == "Distribuído Linear":
                carga = Linear(valor("q1"), valor("q2"), valor("inicio"), valor("fim"))
                dados = {"x1": carga.posicao_inicial, "x2": carga.posicao_final, "q1": carga.intensidade_inicial, "q2": carga.intensidade_final}
                tipo_desenho = "linear"
            else:
                carga = Momento_Binario(valor("intensidade"), valor("posicao"))
                dados = {"x": carga.posicao, "valor": carga.intensidade}
                tipo_desenho = "momento"
            viga.adicionar_carga(carga)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            return

        elementos_viga.adicionar_carga(tipo_desenho, dados)
        lista_cargas.insert(tk.END, str(carga))
        for entrada in campos.values():
            entrada.delete(0, tk.END)

    def remover_carregamento_interface():
        global viga
        selecionado = lista_cargas.curselection()
        if not selecionado or viga is None:
            return
        indice = selecionado[0]
        if remover_carga(viga, indice):
            lista_cargas.delete(indice)
            elementos_viga.remover_carga(indice)

    def calcular_reacoes_e_diagramas():
        if viga is None:
            messagebox.showerror("Erro", "Crie a viga primeiro.")
            return
        try:
            reacoes = viga.calcular_reacoes_2_apoios()
            xs, vs, ms = plotar_diagramas(fig_diagramas, canvas_diagramas, viga)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            return

        elementos_viga.atualizar()
        v_max = max(vs) if vs else 0.0
        v_min = min(vs) if vs else 0.0
        m_max = max(ms) if ms else 0.0
        m_min = min(ms) if ms else 0.0

        linhas = []
        if reacoes["tipo"] == "engaste":
            linhas.append(f"Reação vertical no engaste: {reacoes['Ry']:.2f} N")
            linhas.append(f"Momento de reação no engaste: {reacoes['M']:.2f} N.m")
        else:
            a1 = reacoes["apoio_1"]
            a2 = reacoes["apoio_2"]
            linhas.append(f"Reação em {a1.tipo} x={a1.posicao:g}: {reacoes['R1']:.2f} N")
            linhas.append(f"Reação em {a2.tipo} x={a2.posicao:g}: {reacoes['R2']:.2f} N")
        linhas.append(f"Força Cortante Máx (+): {v_max:.2f} N")
        linhas.append(f"Força Cortante Mín (-): {v_min:.2f} N")
        linhas.append(f"Momento Fletor Máx (+): {m_max:.2f} N.m")
        linhas.append(f"Momento Fletor Mín (-): {m_min:.2f} N.m")
        resultados_var.set("   |   ".join(linhas))

    # =============================== WIDGETS ESQUERDA ========================
    tk.Button(lateral_esquerda, text="Criar Viga", width=20, command=criar_viga).pack(anchor="w", padx=12, pady=10)

    tk.Label(lateral_esquerda, text="APOIOS", font=("Arial", 8, "bold"), bg="#f4f4f4").pack(anchor="w", padx=12, pady=5)
    tk.Label(lateral_esquerda, text="Tipo", bg="#f4f4f4").pack(anchor="w", padx=12)
    combo_apoio = ttk.Combobox(lateral_esquerda, values=["pino", "rolete", "engaste"], state="readonly", width=16)
    combo_apoio.pack(anchor="w", padx=12, pady=5)
    combo_apoio.current(0)

    tk.Label(lateral_esquerda, text="Posição", bg="#f4f4f4").pack(anchor="w", padx=12, pady=5)
    entry_pos = tk.Entry(lateral_esquerda, width=18)
    entry_pos.pack(anchor="w", padx=12, pady=5)

    lista_apoios = tk.Listbox(lateral_esquerda, width=25, height=6)
    lista_apoios.pack(pady=8, padx=5)

    frame_botoes_apoios = tk.Frame(lateral_esquerda, bg="#f4f4f4")
    frame_botoes_apoios.pack(anchor="w", padx=4)
    tk.Button(frame_botoes_apoios, text="Adicionar", command=adicionar_apoio_interface).pack(side="left", padx=2)
    tk.Button(frame_botoes_apoios, text="Remover", command=remover_apoio_interface).pack(side="left", padx=2)

    tk.Label(lateral_esquerda, text="REAÇÕES (calculadas)", font=("Arial", 8, "bold"), bg="#f4f4f4").pack(anchor="w", padx=12, pady=12)
    tk.Button(lateral_esquerda, text="Calcular Reações", width=20, command=calcular_reacoes_e_diagramas).pack(anchor="w", padx=12, pady=8)

    # =============================== WIDGETS DIREITA =========================
    tk.Label(lateral_direita, text="CARREGAMENTOS", font=("Arial", 8, "bold"), bg="#f4f4f4").pack(anchor="center", pady=16)
    tk.Label(lateral_direita, text="Tipo de carregamento", bg="#f4f4f4").pack(anchor="w", padx=12)
    combo_carregamento = ttk.Combobox(
        lateral_direita,
        values=["Concentrado", "Distribuído Constante", "Distribuído Linear", "Momento Binário"],
        state="readonly",
        width=22,
    )
    combo_carregamento.pack(anchor="w", padx=12, pady=5)
    combo_carregamento.current(0)

    campos = {}
    frame_parametros = tk.Frame(lateral_direita, bg="#f4f4f4")
    frame_parametros.pack(anchor="w", padx=12, pady=8)
    combo_carregamento.bind("<<ComboboxSelected>>", atualizar_parametros)
    atualizar_parametros()

    tk.Button(lateral_direita, text="Adicionar carregamento", command=adicionar_carregamento_interface).pack(pady=8)
    tk.Label(lateral_direita, text="Lista de cargas:", bg="#f4f4f4").pack(pady=8)
    lista_cargas = tk.Listbox(lateral_direita, width=30, height=15)
    lista_cargas.pack(padx=5)
    tk.Button(lateral_direita, text="Remover Carregamento", command=remover_carregamento_interface).pack(pady=8)

    screen.mainloop()