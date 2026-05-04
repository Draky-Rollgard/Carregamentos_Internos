#pip install tk

import os
from tkinter import*
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#==================================================
screen = Tk()

l = 1080
h = 700

largura_tela = screen.winfo_screenwidth()
altura_tela = screen.winfo_screenheight()
pos_x = int((largura_tela / 2) - (l / 2))
pos_y = int((altura_tela / 2) - (h / 2))

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
Label(lateral_esquerda, text="DADOS DA VIGA", font=("Arial", 10, "bold"), bg="#f4f4f4").pack(pady=15, padx=15)

Label(lateral_esquerda, text="Comprimento:", bg="#f4f4f4").pack()
Entry(lateral_esquerda).pack(pady=5)

Label(lateral_esquerda, text="Referencial:", bg="#f4f4f4").pack()
Entry(lateral_esquerda).pack(pady=5)

# Apoios
Label(lateral_esquerda, text="APOIOS",font=("Arial", 10, "bold"), bg="#f4f4f4").pack(pady=10)

Label(lateral_esquerda, text="Tipo:", bg="#f4f4f4").pack()

combo_apoio = ttk.Combobox(
    lateral_esquerda,
    values=["Pino", "Rolete", "Engastado"],
    state="readonly",
    width=18
)
combo_apoio.pack(pady=5)
combo_apoio.current(0)


Label(lateral_esquerda, text="Posição:", bg="#f4f4f4").pack()
entry_pos = Entry(lateral_esquerda, width=20)
entry_pos.pack(pady=5)

lista_apoios = Listbox(lateral_esquerda, width=25, height=6)
lista_apoios.pack(pady=8, padx=5)

def adicionar_apoio():
    tipo = combo_apoio.get()
    pos = entry_pos.get()

    texto = f"{tipo} em x={pos}"
    lista_apoios.insert(END, texto)

    entry_pos.delete(0, END)

Button(
    lateral_esquerda,
    text="Adicionar Apoio",
    command=adicionar_apoio
).pack(pady=5)



# ---------  Lateral Direita  --------------
lateral_direita = Frame(screen, bg="#f4f4f4", width=200)
lateral_direita.pack(side="right", fill="y")

# CARREGAMENTOS | LISTA DE CARREGAMENTOS
Label(lateral_direita, text="CARREGAMENTOS", font=("Arial", 10, "bold"), bg="#f4f4f4").pack(pady=15, padx=15)

Button(lateral_direita, text="Força Concentrada", width=22).pack(pady=5)
Button(lateral_direita, text="Carga Distribuída", width=22).pack(pady=5)
Button(lateral_direita, text="Momento", width=22).pack(pady=5)

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

# ----- Desenho -----
painel_desenho = LabelFrame(
    coluna_esquerda,
    text="Desenho do Carregamento",
    font=("Arial", 10, "bold"),
    bg="white",
    relief="solid",
    bd=1
)

painel_desenho.pack(fill="both", expand=True, padx=5, pady=(0,10))

Label(
    painel_desenho,
    text="Área para mostrar a viga e os carregamentos",
    bg="white"
).pack(expand=True)

# ----- Resultados -----
painel_resultados = LabelFrame(
    coluna_esquerda,
    text="Resultados",
    font=("Arial", 10, "bold"),
    bg="white",
    relief="solid",
    bd=1,
    height=120
)

painel_resultados.pack(fill="x", padx=5, pady=(0,5))
painel_resultados.pack_propagate(False)

Label(
    painel_resultados,
    text="Área para reações, cortante e momento",
    bg="white"
).pack(expand=True)

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

#=================
screen.mainloop()