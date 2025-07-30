import tkinter as tk
from tkinter import messagebox, ttk
from funcoes_importantes import ( inicializar_objetos_pessoas, iniciar_simulacao, simular_1_mes, resetar_simulacao)
import json
import csv
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Simulador de relações de Mercado")
root.geometry("1400x900")


main_frame = tk.Frame(root) 
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


title_label = tk.Label(main_frame, 
                       text="SIMULADOR DE RELAÇÕES DE MERCADO", 
                       font=("Arial", 24), 
                       fg="black")
title_label.pack(pady=(0,15))

# Frame para os controles de simulação
controles_frame = tk.Frame(main_frame)
controles_frame.pack(pady=(0, 20))

# Label e Entry para o número de meses para simular
meses_simular_label = tk.Label(controles_frame, 
                                text="Meses para simular:",
                                font=("Arial", 16),
                                fg="black")
meses_simular_label.pack(side=tk.LEFT, padx=(0, 15))
meses_entry = tk.Entry(controles_frame, 
                                font=("Arial", 16), 
                                width=5)


meses_entry.pack(side=tk.LEFT, padx=(0, 15))
meses_entry.insert(0, "1")

total_meses_simulados = 0

lista_pessoas_simulacao = []

def iniciar_simulacao_wrapper():
    global total_meses_simulados, lista_pessoas_simulacao
    total_meses_simulados = iniciar_simulacao(total_meses_simulados, meses_entry, valor_mes_simulados, atualizar_graficos)

def simular_1_mes_wrapper():
    global total_meses_simulados, lista_pessoas_simulacao
    total_meses_simulados = simular_1_mes(total_meses_simulados, valor_mes_simulados, atualizar_graficos)

def resetar_simulacao_wrapper():
    global total_meses_simulados, lista_pessoas_simulacao, pessoas_dados_iniciais
    total_meses_simulados = resetar_simulacao(meses_entry, valor_mes_simulados, pessoas_dados_iniciais, atualizar_graficos)

simular_button = tk.Button(controles_frame, 
                          text="Simular",
                          font=("Arial", 16),
                          command=iniciar_simulacao_wrapper)
simular_button.pack(side=tk.LEFT, padx=(0, 15))


#Simular 1 mês 
simular_1_mes_button = tk.Button(controles_frame, 
                                 text="Simular 1 mês",  
                                    font=("Arial", 16),
                                    command=simular_1_mes_wrapper)
simular_1_mes_button.pack(side=tk.LEFT, padx=(0, 15))


#Resetar
reset_button = tk.Button(controles_frame,
                        text="Resetar",
                        font=("Arial", 16),
                        command=resetar_simulacao_wrapper)
reset_button.pack(side=tk.LEFT, padx=(0, 15))


#Monstrando meses simulados
meses_simulados_label = tk.Label(controles_frame, 
                                text="Meses Simulados:",
                                font=("Arial", 16),
                                fg="black")
meses_simulados_label.pack(side=tk.LEFT, padx=(0, 15))
valor_mes_simulados = tk.StringVar()
valor_mes_simulados.set("0")
meses_simulados_value = tk.Label(controles_frame, 
                                textvariable=valor_mes_simulados,
                                font=("Arial", 16),
                                fg="black")
meses_simulados_value.pack(side=tk.LEFT, padx=(0, 15))

# Parte das Abas

# Criando o notebook com as abas (centralizado)
notebook = ttk.Notebook(main_frame)
notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

# Aba de Categorias
categoria_frame = tk.Frame(notebook)
notebook.add(categoria_frame, text="📊 Categorias")

# Frame principal para categorias
categoria_main_frame = tk.Frame(categoria_frame)
categoria_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Título da seção
categoria_title = tk.Label(categoria_main_frame, 
                          text="Divisão da Renda Mensal", 
                          font=("Arial", 18, "bold"), 
                          fg="#2E4057")
categoria_title.pack(pady=(0, 15))

# Frame para o texto das categorias com scrollbar
categoria_text_frame = tk.Frame(categoria_main_frame)
categoria_text_frame.pack(fill=tk.BOTH, expand=True)

categoria_text = tk.Text(categoria_text_frame, 
                        font=("Arial", 12), 
                        wrap=tk.WORD,
                        bg="#F8F9FA",
                        relief=tk.SOLID,
                        borderwidth=1)
categoria_scrollbar = ttk.Scrollbar(categoria_text_frame, orient="vertical", command=categoria_text.yview)
categoria_text.configure(yscrollcommand=categoria_scrollbar.set)

categoria_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
categoria_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Carregando os dados de categorias do arquivo JSON
def carregar_categorias():
    with open("src/dados/categorias.json", "r", encoding="utf-8") as file:
        return json.load(file)

categorias = carregar_categorias()

categoria_content = "CATEGORIAS\n\nDivisão da renda mensal:\n\n"
for categoria, percentual in categorias.items():
    categoria_content += f"{categoria}: {percentual * 100:.1f}%\n"

categoria_content += "\nTotal: 90.0% da renda mensal"

categoria_text.insert(tk.END, categoria_content)
categoria_text.config(state=tk.DISABLED)  # Torna o texto somente para leitura

# Aba de Pessoas
pessoas_frame = tk.Frame(notebook)
notebook.add(pessoas_frame, text="👥 Pessoas")

# Frame principal para pessoas
pessoas_main_frame = tk.Frame(pessoas_frame)
pessoas_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Título da seção
pessoas_title = tk.Label(pessoas_main_frame, 
                        text="Pessoas e Patrimônio", 
                        font=("Arial", 18, "bold"), 
                        fg="#2E4057")
pessoas_title.pack(pady=(0, 15))

# Frame para a tabela com scrollbars
tabela_frame = tk.Frame(pessoas_main_frame)
tabela_frame.pack(fill=tk.BOTH, expand=True)

# Criando tabela de pessoas com scrollbars  
colunas_pessoas = ("Nome", "Patrimônio", "Salário", "Renda Mensal", "Conforto")
tabela_pessoas = ttk.Treeview(tabela_frame, columns=colunas_pessoas, show="headings", height=15)

# Configurando scrollbars
scrollbar_vertical = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela_pessoas.yview)
scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela_pessoas.xview)
tabela_pessoas.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

# Posicionando tabela e scrollbars
tabela_pessoas.grid(row=0, column=0, sticky="nsew")
scrollbar_vertical.grid(row=0, column=1, sticky="ns")
scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

tabela_frame.grid_rowconfigure(0, weight=1)
tabela_frame.grid_columnconfigure(0, weight=1)

# Configurando colunas da tabela
for col in colunas_pessoas:
    tabela_pessoas.heading(col, text=col)
    tabela_pessoas.column(col, anchor=tk.CENTER, width=150)

# Ajustando larguras específicas das colunas
tabela_pessoas.column("Nome", width=200)
tabela_pessoas.column("Patrimônio", width=150)
tabela_pessoas.column("Salário", width=150)
tabela_pessoas.column("Renda Mensal", width=150)
tabela_pessoas.column("Conforto", width=100)


def carregar_pessoas():
    with open("src/dados/pessoas.txt", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]  # Remove espaços extras
        return [
            {
                "Nome": row["nome"].strip(),
                "Patrimônio": f"R$ {int(row['patrimonio']):,}".replace(",", "."),
                "Salário": f"R$ {int(row['salario']):,}".replace(",", "."),
                # Renda Mensal inicial: salário + 0.5% do patrimônio
                "Renda Mensal": f"R$ {int(int(row['salario']) + int(row['patrimonio']) * 0.005):,}".replace(",", "."),
                "Conforto": "0,0%"
            }
            for row in reader
        ]

# Carregando os dados de pessoas
pessoas = carregar_pessoas()

# Inicializando variáveis globais para simulação
pessoas_dados_iniciais = carregar_pessoas()
lista_pessoas_simulacao = inicializar_objetos_pessoas(pessoas_dados_iniciais)

# Inserindo dados na tabela
tabela_pessoas.delete(*tabela_pessoas.get_children())
for i, pessoa in enumerate(pessoas):
    valores = (
        pessoa["Nome"],
        pessoa["Patrimônio"],
        pessoa["Salário"],
        pessoa["Renda Mensal"],
        pessoa["Conforto"]
    )
    tags = ("even",) if i % 2 == 0 else ()
    tabela_pessoas.insert("", tk.END, values=valores, tags=tags)

# Configurando tags para cores alternadas
tabela_pessoas.tag_configure("even", background="#F8F9FA")

# Aba de Empresas
empresas_frame = tk.Frame(notebook)
notebook.add(empresas_frame, text="🏢 Empresas")

# Frame principal para empresas
empresas_main_frame = tk.Frame(empresas_frame)
empresas_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Título da seção
empresas_title = tk.Label(empresas_main_frame, 
                         text="Empresas e Produtos", 
                         font=("Arial", 18, "bold"), 
                         fg="#2E4057")
empresas_title.pack(pady=(0, 15))

# Frame para a tabela com scrollbars
tabela_empresas_frame = tk.Frame(empresas_main_frame)
tabela_empresas_frame.pack(fill=tk.BOTH, expand=True)

# Criando tabela de empresas com scrollbars  
colunas_empresas = ("Categoria", "Empresa", "Produto/Serviço", "Custo", "Qualidade")
tabela_empresas = ttk.Treeview(tabela_empresas_frame, columns=colunas_empresas, show="headings", height=15)

# Configurando scrollbars
scrollbar_vertical_empresas = ttk.Scrollbar(tabela_empresas_frame, orient="vertical", command=tabela_empresas.yview)
scrollbar_horizontal_empresas = ttk.Scrollbar(tabela_empresas_frame, orient="horizontal", command=tabela_empresas.xview)
tabela_empresas.configure(yscrollcommand=scrollbar_vertical_empresas.set, xscrollcommand=scrollbar_horizontal_empresas.set)

# Posicionando tabela e scrollbars
tabela_empresas.grid(row=0, column=0, sticky="nsew")
scrollbar_vertical_empresas.grid(row=0, column=1, sticky="ns")
scrollbar_horizontal_empresas.grid(row=1, column=0, sticky="ew")

tabela_empresas_frame.grid_rowconfigure(0, weight=1)
tabela_empresas_frame.grid_columnconfigure(0, weight=1)

# Configurando colunas da tabela
for col in colunas_empresas:
    tabela_empresas.heading(col, text=col)
    tabela_empresas.column(col, anchor=tk.CENTER, width=150)

# Ajustando larguras específicas das colunas
tabela_empresas.column("Categoria", width=150)
tabela_empresas.column("Empresa", width=180)
tabela_empresas.column("Produto/Serviço", width=180)
tabela_empresas.column("Custo", width=100)
tabela_empresas.column("Qualidade", width=100)

def carregar_empresas():
    with open("src/dados/empresas.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        return [
            {
                "Categoria": row[0],
                "Empresa": row[1],
                "Produto/Serviço": row[2],
                "Custo": f"R$ {float(row[3]):,.2f}".replace(",", "."),
                "Qualidade": row[4]
            }
            for row in reader
        ]

empresas = carregar_empresas()

# Inserindo dados na tabela
tabela_empresas.delete(*tabela_empresas.get_children())
for i, empresa in enumerate(empresas):
    valores = (
        empresa["Categoria"],
        empresa["Empresa"],
        empresa["Produto/Serviço"],
        empresa["Custo"],
        empresa["Qualidade"]
    )
    tags = ("even",) if i % 2 == 0 else ()
    tabela_empresas.insert("", tk.END, values=valores, tags=tags)

# Configurando tags para cores alternadas
tabela_empresas.tag_configure("even", background="#F8F9FA")

# Aba de Gráficos
graficos_frame = tk.Frame(notebook)
notebook.add(graficos_frame, text="📈 Gráficos")

# Frame principal para gráficos
graficos_main_frame = tk.Frame(graficos_frame)
graficos_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


graficos_title = tk.Label(graficos_main_frame, 
                         text="", 
                         font=("Arial", 18, "bold"), 
                         fg="#2E4057")
graficos_title.pack(pady=(0, 5))

# Container principal para organizar os gráficos em grid para garantir tamanhos iguais
graficos_container = tk.Frame(graficos_main_frame)
graficos_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Grid para garantir que as linhas tenham o mesmo tamanho
graficos_container.grid_rowconfigure(0, weight=1)
graficos_container.grid_rowconfigure(1, weight=1)
graficos_container.grid_columnconfigure(0, weight=1)

# Dois frames separados com bordas para os gráficos
grafico1_frame = tk.Frame(graficos_container, borderwidth=2, relief=tk.RIDGE, bg="#F8F9FA")
grafico1_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

grafico2_frame = tk.Frame(graficos_container, borderwidth=2, relief=tk.RIDGE, bg="#F8F9FA")
grafico2_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Função para configuração idêntica dos gráficos
def configurar_grafico(figura, eixo, frame):
    canvas = FigureCanvasTkAgg(figura, master=frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    return canvas

# Ajustando o tamanho da figura 
fig1 = Figure(figsize=(8, 2.5), dpi=100)
ax1 = fig1.add_subplot(111) # Um único gráfico na figura
fig1.subplots_adjust(top=0.85, bottom=0.25, left=0.1, right=0.9)

# Tamanho da figura para o segundo gráfico 
fig2 = Figure(figsize=(8, 2.5), dpi=100)
ax2 = fig2.add_subplot(111) # Um único gráfico na figura
fig2.subplots_adjust(top=0.85, bottom=0.25, left=0.1, right=0.9)

# Canvas para ambos os gráficos 
canvas1 = configurar_grafico(fig1, ax1, grafico1_frame)
canvas2 = configurar_grafico(fig2, ax2, grafico2_frame)

# Lógica de simulação
def simular_mudancas():
    global pessoas
    for pessoa in pessoas:
        patrimonio_atual = int(pessoa["Patrimônio"].replace("R$ ", "").replace(".", ""))
        salario_atual = int(pessoa["Salário"].replace("R$ ", "").replace(".", ""))

        # Simulando mudanças
        patrimonio_atual += random.randint(-1000, 5000)
        salario_atual += random.randint(-500, 1000)

        pessoa["Patrimônio"] = f"R$ {patrimonio_atual:,}".replace(",", ".")
        pessoa["Salário"] = f"R$ {salario_atual:,}".replace(",", ".")
        pessoa["Renda Mensal"] = f"R$ {int(salario_atual * 1.1):,}".replace(",", ".")

    # Atualizando a tabela
    tabela_pessoas.delete(*tabela_pessoas.get_children())
    for i, pessoa in enumerate(pessoas):
        valores = (
            pessoa["Nome"],
            pessoa["Patrimônio"],
            pessoa["Salário"],
            pessoa["Renda Mensal"],
            pessoa["Conforto"]
        )
        tags = ("even",) if i % 2 == 0 else ()
        tabela_pessoas.insert("", tk.END, values=valores, tags=tags)

# Melhorando o visual da interface
root.configure(bg="#F0F0F0")
main_frame.configure(bg="#F0F0F0")

# Atualizando o título
categoria_title.configure(fg="#1E88E5")
pessoas_title.configure(fg="#1E88E5")
empresas_title.configure(fg="#1E88E5")

# Atualizando botões
simular_button.configure(bg="#4CAF50", fg="white", activebackground="#45A049")
simular_1_mes_button.configure(bg="#4CAF50", fg="white", activebackground="#45A049")
reset_button.configure(bg="#F44336", fg="white", activebackground="#E53935")

def atualizar_tabela_pessoas(lista_pessoas_obj):
    tabela_pessoas.delete(*tabela_pessoas.get_children())
    for i, pessoa in enumerate(lista_pessoas_obj):
        valores = (
            pessoa.nome,
            f"R$ {int(pessoa.patrimonio):,}".replace(",", "."),
            f"R$ {int(pessoa.salario):,}".replace(",", "."),
            f"R$ {int(pessoa.rendimento_mensal):,}".replace(",", "."),
            f"{pessoa.conforto:.1f}"
        )
        tags = ("even",) if i % 2 == 0 else ()
        tabela_pessoas.insert("", tk.END, values=valores, tags=tags)

def atualizar_graficos(lista_pessoas):
    ax1.clear()
    ax2.clear()

    # Extrai diretamente dos objetos Pessoa
    nomes = [p.nome for p in lista_pessoas]
    salarios = [p.salario for p in lista_pessoas]
    rendimentos = [p.rendimento_mensal for p in lista_pessoas]
    conforto = [p.conforto for p in lista_pessoas]

    x = range(len(nomes)) # eixo X

    # Função para configuração comum dos gráficos
    def configurar_estilo_grafico(ax):
        ax.set_ylabel("")
        ax.set_xticks([])
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_frame_on(True)
    
    nomes = [p.nome for p in lista_pessoas]
    salarios = [p.salario for p in lista_pessoas]

    # GRÁFICO 1: Salário e Rendimentos 
    ax1.bar(x, salarios, color='limegreen', label='Salário')
    ax1.bar(x, rendimentos, bottom=salarios, color='darkviolet', label='Rendimentos')
    
    tick_values = [0, 20282, 40565, 60847, 81129, 101411]
    ax1.set_ylim(0, 101411)
    ax1.set_yticks(tick_values)
    ax1.set_yticklabels(['R$ 0', 'R$ 20282', 'R$ 40565', 'R$ 60847', 'R$ 81129', 'R$ 101411'])
    
    configurar_estilo_grafico(ax1)

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=2)

    # GRÁFICO 2: Nível de Conforto 
    ax2.bar(x, conforto, color='dodgerblue', label='Conforto')
    
    ax2.set_ylim(0, 40)  
    ax2.set_yticks([0, 8, 16, 24, 32, 40])
    ax2.set_yticklabels(['0.0', '8.0', '16.0', '24.0', '32.0', '40.0'])
    
    configurar_estilo_grafico(ax2)
    
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=1)


    canvas1.draw()
    canvas2.draw()

    atualizar_tabela_pessoas(lista_pessoas)

atualizar_graficos(lista_pessoas_simulacao)

root.mainloop()