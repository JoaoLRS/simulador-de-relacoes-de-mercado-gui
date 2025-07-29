import tkinter as tk
from tkinter import messagebox, ttk
from funcoes_importantes import *

#TODO: Ana se possivel, as funções devem ser importadas do arquivo funcoes_importantes.py, caso vc n 
# conseguir fazer isso, a gente pode deixar tudo aqui mesmo, eu n fiz isso pq, priorizei a criação
#inicial da interface gráfica e a funcionalidade de simulação 

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

def iniciar_simulacao():
    global total_meses_simulados
    try:
        meses = int(meses_entry.get())
        if meses <= 0:
            messagebox.showerror("Erro", "O número de meses deve ser maior que zero!")
            return
        
        messagebox.showinfo("Simulação", f"Simulação iniciada para {meses} meses!")
        
        total_meses_simulados += meses
        valor_mes_simulados.set(str(total_meses_simulados))
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de meses!")

def simular_1_mes():
    global total_meses_simulados
    # Simula especificamente 1 mês
    messagebox.showinfo("Simulação", "Simulação de 1 mês iniciada!")
    
    total_meses_simulados += 1
    valor_mes_simulados.set(str(total_meses_simulados))

def resetar_simulacao():
    global total_meses_simulados
    meses_entry.delete(0, tk.END)
    meses_entry.insert(0, "1")
    
    # Reseta o contador de meses simulados
    total_meses_simulados = 0
    valor_mes_simulados.set("0")
    
    messagebox.showinfo("Reset", "Simulação resetada!")

simular_button = tk.Button(controles_frame, 
                          text="Simular",
                          font=("Arial", 16),
                          command=iniciar_simulacao)
simular_button.pack(side=tk.LEFT, padx=(0, 15))


#Simular 1 mês 
simular_1_mes_button = tk.Button(controles_frame, 
                                 text="Simular 1 mês",  
                                    font=("Arial", 16),
                                    command=simular_1_mes)
simular_1_mes_button.pack(side=tk.LEFT, padx=(0, 15))


#Resetar
reset_button = tk.Button(controles_frame,
                        text="Resetar",
                        font=("Arial", 16),
                        command=resetar_simulacao)
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
                          text="CATEGORIAS DE GASTOS", 
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

# Conteúdo melhorado das categorias TODO Os dados de categoria deve ser inportados
categoria_content = """CATEGORIAS

Divisão da renda mensal:

Moradia: 35.0%
Alimentação: 25.0%
Transporte: 10.0%
Saúde: 10.0%
Educação: 10.0%

Total: 90.0% da renda mensal"""

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
                        text="PESSOAS NO SISTEMA", 
                        font=("Arial", 18, "bold"), 
                        fg="#2E4057")
pessoas_title.pack(pady=(0, 15))

# Frame para a tabela com scrollbars
tabela_frame = tk.Frame(pessoas_main_frame)
tabela_frame.pack(fill=tk.BOTH, expand=True)

# Criando tabela de pessoas com scrollbars  TODO Todos esses dados deve ser inportados
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

# Dados das pessoas com formatação melhorada TODO Todos esses dados deve ser inportados
dados_pessoas = [
    ("Carla de Carvalho", "R$ 20.000.000,00", "R$ 0,00", "R$ 100.000,00", "0,0%"),
    ("Francisca Costa", "R$ 20.000.000,00", "R$ 0,00", "R$ 100.000,00", "0,0%"),
    ("Adriana Santos", "R$ 200.000,00", "R$ 100.000,00", "R$ 101.000,00", "0,0%"),
    ("João Silva", "R$ 50.000,00", "R$ 5.000,00", "R$ 5.500,00", "0,0%"),
    ("Maria Oliveira", "R$ 150.000,00", "R$ 8.000,00", "R$ 8.800,00", "0,0%")
]

# Inserindo dados na tabela
for i, linha in enumerate(dados_pessoas):
    # Alternando cores das linhas para melhor visualização
    if i % 2 == 0:
        item = tabela_pessoas.insert("", tk.END, values=linha, tags=("even",))
    else:
        item = tabela_pessoas.insert("", tk.END, values=linha)

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
                         text="EMPRESAS NO MERCADO", 
                         font=("Arial", 18, "bold"), 
                         fg="#2E4057")
empresas_title.pack(pady=(0, 15))

# Placeholder para futuras funcionalidades de empresas
empresas_placeholder = tk.Label(empresas_main_frame, 
                               text="📊 Falta criar a logica para os GRAFICOS", 
                               font=("Arial", 14),
                               fg="#6C757D")
empresas_placeholder.pack(expand=True)



root.mainloop()