#pip install tk

import os
from tkinter import*
from tkinter import ttk
import customtkinter as ctk

from logica.carregamentos import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#==================================================
#screen = Tk()
screen = ctk.CTk()

l = 1080
h = 700

largura_tela = screen.winfo_screenwidth()
altura_tela = screen.winfo_screenheight()
pos_x = int((largura_tela / 2) - (l / 2))
pos_y = int((altura_tela / 2) - (h / 1.7))

screen.geometry(f"{l}x{h}+{pos_x}+{pos_y}")
screen.title("Projeto_Carregamentos_Internos")
screen.config(bg="lightblue")
#screen.geometry("1080x700")

#====================== Objeto de estudo ========================
topo = Frame(screen, bg="#1c2b39", height=25)
topo.pack(fill="x")

Label(
    topo,
    text="Mecânica Geral\nEstática - Carregamentos internos",
    fg="white",
    bg="#1c2b39",
    font=("Arial", 10, "bold")
).pack(pady=10)

#======================Menu==========================
menu_principal = Menu(screen)
screen.config(menu=menu_principal)

# Menu de arquivo
menu_arq = Menu(menu_principal, tearoff=0)

menu_arq.add_command(
    label="Novo",
    command=lambda: print("Clique em novo")
)

menu_arq.add_command(
    label="Abrir",
    command=lambda: print("Clique em abrir")
)

menu_arq.add_separator()
menu_arq.add_command(
    label="Sair",
    command=screen.quit
)

menu_principal.add_cascade(
    label="Arquivo",
    menu=menu_arq
)

# -------- Menu Editar --------
menu_editar = Menu(menu_principal, tearoff=0)

menu_principal.add_cascade(
    label="Editar",
    menu=menu_editar
)









#======================= Laterais ==========================
''' Usar para interfaceamento 
    de imputação de dados e
    escolha de Carregamentos'''











# ---------  Lateral Esquerda  --------------
lateral_esquerda = Frame(screen, bg="#f4f4f4", width=200)
lateral_esquerda.pack(side="left", fill="y")

# DADOS DA VIGA | APOIOS
# geometria
Label(
    lateral_esquerda,
    text="GEOMETRIA",
    font=("Arial", 8, "bold"),
    bg="#f4f4f4"
    ).pack(anchor="w",pady=10, padx=15)
Label(
    lateral_esquerda, 
    text="Comprimento da viga",
    bg="#f4f4f4").pack(anchor="w",padx=15)
Entry(lateral_esquerda).pack(anchor="w",padx=15, pady=5)

Label(
    lateral_esquerda, 
    text="Referencial",
    bg="#f4f4f4").pack(anchor="w",padx=15)
Entry(lateral_esquerda).pack(anchor="w",padx=15, pady=5)


# Apoios
Label(
    lateral_esquerda,
    text="APOIOS",
    font=("Arial", 8, "bold"),
    bg="#f4f4f4").pack(anchor="w",padx=15, pady=5)

Label(
    lateral_esquerda,
    text="Tipo",
    bg="#f4f4f4").pack(anchor="w",padx=15)

combo_apoio = ttk.Combobox(
    lateral_esquerda,
    values=["Pino", "Rolete", "Engastado"],
    state="readonly",
    width=16
)
combo_apoio.pack(anchor="w",padx=15, pady=5)
combo_apoio.current(0)

#Apoio - input posicao
Label(lateral_esquerda, text="Posição", bg="#f4f4f4").pack(anchor="w",padx=15, pady=5)
entry_pos = Entry(lateral_esquerda, width=20)
entry_pos.pack(anchor="w",padx=15, pady=5)

# Apoios - listar
lista_apoios = Listbox(lateral_esquerda, width=25, height=6)
lista_apoios.pack(pady=8, padx=5)

# Apoios - add & rem
def adicionar_apoio():
    tipo = combo_apoio.get()
    pos = entry_pos.get()

    texto = f"{tipo} em x={pos}"
    lista_apoios.insert(END, texto)

    entry_pos.delete(0, END)

def remover_apoio():

    selecionado = lista_apoios.curselection()

    if selecionado:
        lista_apoios.delete(selecionado)

# Apoios - botões add & rem
frame_botoes_apoio = Frame(
    lateral_esquerda,
    bg="#f4f4f4"
)
frame_botoes_apoio.pack(pady=5)

Button(
    frame_botoes_apoio,
    text="Adicionar",
    width=10,
    command=adicionar_apoio
).pack(
    side="left",
    padx=3
)

Button(
    frame_botoes_apoio,
    text="Remover",
    width=10,
    command=remover_apoio
).pack(
    side="left",
    padx=3
)

# Lista dados calculados de reações na viga (por somatorio Força ou Momento)
Label(
    lateral_esquerda,
    text="REAÇÕES (calculadas)",
    font=("Arial", 8, "bold"),
    bg="#f4f4f4"
    ).pack(anchor="w",pady=10, padx=15)

lista_reacoes = Listbox(lateral_esquerda, width=25, height=6)
lista_reacoes.pack(pady=8, padx=5)



















# ---------  Lateral Direita  --------------
lateral_direita = Frame(screen, bg="#f4f4f4", width=200)
lateral_direita.pack(side="right", fill="y")

# CARREGAMENTOS | LISTA DE CARREGAMENTOS
Label(lateral_direita, text="CARREGAMENTOS", font=("Arial", 8, "bold"), bg="#f4f4f4").pack(pady=15, padx=15)


# Tipagem dos carregamentos
Label(
    lateral_direita,
    text="Tipo de carregamento",
    bg="#f4f4f4"
).pack(anchor="w", padx=15, pady=(10,0))

combo_carregamento = ttk.Combobox(
    lateral_direita,
    values=[
        "Concentrado",
        "Distribuído Constante",
        "Distribuído Linear",
        "Momento Binário"
    ],
    state="readonly",
    width=22
)

combo_carregamento.pack(anchor="w", padx=15, pady=5)
combo_carregamento.current(0)

frame_parametros = Frame(
    lateral_direita,
    bg="#f4f4f4"
)

frame_parametros.pack(
    fill="x",
    padx=15,
    pady=10
)

campos = {}

def atualizar_parametros(event=None):

    # limpa widgets antigos
    for widget in frame_parametros.winfo_children():
        widget.destroy()

    campos.clear()

    tipo = combo_carregamento.get()

    # ===========CONCENTRADO===============

    if tipo == "Concentrado":

        Label(
            frame_parametros,
            text="Intensidade",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["intensidade"] = Entry(frame_parametros)
        campos["intensidade"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["posicao"] = Entry(frame_parametros)
        campos["posicao"].pack(fill="x", pady=3)

    # ===========DISTRIBUÍDO CONSTANTE===============
   
    elif tipo == "Distribuído Constante":

        Label(
            frame_parametros,
            text="Intensidade",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["intensidade"] = Entry(frame_parametros)
        campos["intensidade"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição inicial",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["inicio"] = Entry(frame_parametros)
        campos["inicio"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição final",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["fim"] = Entry(frame_parametros)
        campos["fim"].pack(fill="x", pady=3)

    # =============DISTRIBUÍDO LINEAR=============
    
    elif tipo == "Distribuído Linear":

        Label(
            frame_parametros,
            text="Intensidade inicial",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["q1"] = Entry(frame_parametros)
        campos["q1"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Intensidade final",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["q2"] = Entry(frame_parametros)
        campos["q2"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição inicial",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["inicio"] = Entry(frame_parametros)
        campos["inicio"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição final",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["fim"] = Entry(frame_parametros)
        campos["fim"].pack(fill="x", pady=3)
    
    # ============Momento Binário==============
        
    elif tipo == "Momento Binário":

        Label(
            frame_parametros,
            text="Momento",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["intensidade"] = Entry(frame_parametros)
        campos["intensidade"].pack(fill="x", pady=3)

        Label(
            frame_parametros,
            text="Posição",
            bg="#f4f4f4"
        ).pack(anchor="w")

        campos["posicao"] = Entry(frame_parametros)
        campos["posicao"].pack(fill="x", pady=3)


combo_carregamento.bind(
    "<<ComboboxSelected>>",
    atualizar_parametros
)

atualizar_parametros()

carregamentos = []
def adicionar_carregamento():

    tipo = combo_carregamento.get()

    # ---------------------------
    # Concentrado
    # ---------------------------
    if tipo == "Concentrado":

        carga = Carregamento_Concentrado(
            intensidade=float(campos["intensidade"].get()),
            posicao=float(campos["posicao"].get())
        )

    # ---------------------------
    # Distribuído Constante
    # ---------------------------
    elif tipo == "Distribuído Constante":

        carga = Constante(
            intensidade=float(campos["intensidade"].get()),
            posicao_inicial=float(campos["inicio"].get()),
            posicao_final=float(campos["fim"].get())
        )

    # ---------------------------
    # Distribuído Linear
    # ---------------------------
    elif tipo == "Distribuído Linear":

        carga = Linear(
            intensidade_inicial=float(campos["q1"].get()),
            intensidade_final=float(campos["q2"].get()),
            posicao_inicial=float(campos["inicio"].get()),
            posicao_final=float(campos["fim"].get())
        )

    # ---------------------------
    # Distribuído Linear
    # ---------------------------

    elif tipo == "Momento Binário":

        carga = Momento_Binario(
            intensidade=float(campos["intensidade"].get()),
            posicao=float(campos["posicao"].get())
        )

    carregamentos.append(carga)
    lista.insert(
        END,
        str(type(carga).__name__)
    )

Button(
    lateral_direita,
    text="Adicionar carregamento",
    command=adicionar_carregamento
).pack(pady=10)

'''
Button(lateral_direita, text="Força Concentrada", width=22).pack(pady=5)
Button(lateral_direita, text="Carga Distribuída", width=22).pack(pady=5)
Button(lateral_direita, text="Momento", width=22).pack(pady=5)
'''

Label(lateral_direita, text="Lista de cargas:", bg="#f4f4f4").pack(pady=10)

lista = Listbox(lateral_direita, width=30, height=15)
lista.pack(padx=5)























#====================== CORPO ==============================
''' Usar para interfaceamento 
    de plotagem das figuras e
    resultado dos cálculos'''
#====================== CORPO ==============================

centro = Frame(screen, bg="lightblue")
centro.pack(fill="both", expand=True, padx=15, pady=15)

# -------- Container principal (divide em esquerda e direita) --------
container_horizontal = Frame(centro, bg="lightblue")
container_horizontal.pack(fill="both", expand=True)

# ================= COLUNA ESQUERDA =================
coluna_esquerda = Frame(container_horizontal, bg="lightblue")
coluna_esquerda.pack(side="left", fill="both", expand=True, padx=(0,5))








# =================== CARD - VIGA, APOIOS E REAÇÕES ===============================
painel_desenho = Frame(coluna_esquerda, bg="#bfc3c7", bd=1)
painel_desenho.pack(fill="both", expand=True, padx=5, pady=(0,10))

# CABEÇALHO
topo_desenho = Frame(painel_desenho, bg="#e9ecef", height=30)
topo_desenho.pack(fill="x")
topo_desenho.pack_propagate(False)
Label(topo_desenho, text="VIGA, APOIOS E REAÇÕES", bg="#e9ecef", fg="black", font=("Arial", 8, "bold")).pack(anchor="w", padx=10, pady=6)

# CORPO
corpo_desenho = Frame(painel_desenho, bg="white")
corpo_desenho.pack(fill="both", expand=True, padx=1, pady=(0,1))
Label(corpo_desenho, text="Área para mostrar a viga e os carregamentos", bg="white", fg="#555555").pack(expand=True)








# ============================== DIAGRAMAS ========================================
painel_diagramas = Frame(coluna_esquerda, bg="#bfc3c7", bd=1)
painel_diagramas.pack(fill="both", expand=True, padx=5, pady=(0,10))

# CABEÇALHO
topo_diagramas = Frame(painel_diagramas, bg="#e9ecef", height=30)
topo_diagramas.pack(fill="x")
topo_diagramas.pack_propagate(False)
Label(topo_diagramas, text="DIAGRAMAS", bg="#e9ecef", fg="black", font=("Arial", 8, "bold")).pack(anchor="w", padx=10, pady=6)

# CORPO
corpo_diagramas = Frame(painel_diagramas, bg="white")
corpo_diagramas.pack(fill="both", expand=True, padx=1, pady=(0,1))
Label(corpo_diagramas, text="Área dos diagramas de Força Cortante e Momento Fletor", bg="white", fg="#555555").pack(expand=True)






# ============================== RESULTADOS ========================================
painel_resultados = Frame(coluna_esquerda, bg="#bfc3c7", bd=1, height=120)
painel_resultados.pack(fill="x", padx=5, pady=(0,10))
painel_resultados.pack_propagate(False)
# CABEÇALHO
topo_resultados = Frame(painel_resultados, bg="#e9ecef", height=30)
topo_resultados.pack(fill="x")
topo_resultados.pack_propagate(False)
Label(topo_resultados, text="RESULTADOS", bg="#e9ecef", fg="black", font=("Arial", 8, "bold")).pack(anchor="w", padx=10, pady=6)

# CORPO
corpo_resultados = Frame(painel_resultados, bg="white")
corpo_resultados.pack(fill="both", expand=True, padx=1, pady=(0,1))
Label(corpo_resultados, text="Área para reações, cortante e momento", bg="white", fg="#555555").pack(expand=True)






'''
# ================= COLUNA DIREITA =================
coluna_direita = Frame(container_horizontal, bg="lightblue")
coluna_direita.pack(side="left", fill="both", expand=True, padx=(5,0))

# ----- Força Cortante -----
painel_FC = LabelFrame(
    coluna_direita,
    text="Força Cortante",
    font=("Arial",10,"bold"),
    bg="white",
    relief="solid",
    bd=1
)

painel_FC.pack(fill="both", expand=True, padx=5, pady=(0,10))

Label(
    painel_FC,
    text="Área do diagrama de Força Cortante",
    bg="white"
).pack(expand=True)

# ----- Momento Fletor -----
painel_MF = LabelFrame(
    coluna_direita,
    text="Momento Fletor",
    font=("Arial",10,"bold"),
    bg="white",
    relief="solid",
    bd=1
)

painel_MF.pack(fill="both", expand=True, padx=5)

Label(
    painel_MF,
    text="Área do diagrama de Momento Fletor",
    bg="white"
).pack(expand=True)
'''




#=================
screen.mainloop()