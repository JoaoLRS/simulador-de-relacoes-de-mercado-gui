import tkinter as tk
from tkinter import messagebox, ttk
import random

lista_de_pessoas_simulacao = []

def inicializar_objetos_pessoas(pessoas_dados):
    from pessoa import Pessoa 
    global lista_de_pessoas_simulacao
    lista_de_pessoas_simulacao.clear()
    for p_dado in pessoas_dados:
        nome = p_dado["Nome"]
        patrimonio = float(p_dado["Patrimônio"].replace("R$ ", "").replace(".", "").replace(",", "."))
        salario = float(p_dado["Salário"].replace("R$ ", "").replace(".", "").replace(",", "."))
        pessoa_obj = Pessoa(nome, patrimonio, salario)
        pessoa_obj.rendimento_mensal = pessoa_obj.patrimonio * 0.005
        lista_de_pessoas_simulacao.append(pessoa_obj)
    return lista_de_pessoas_simulacao

def simular_1_mes(total_meses_simulados, valor_mes_simulados, callback_atualizar_graficos):
    global lista_de_pessoas_simulacao

    # Lógica de simulação de 1 mês 
    for pessoa in lista_de_pessoas_simulacao:
        
        # LÓGICA DE RENDIMENTO: rendimento extra de 0.5% do patrimônio
        rendimento_extra = pessoa.patrimonio * 0.005
        renda_total_recebida = pessoa.salario + rendimento_extra
        pessoa.rendimento_mensal = rendimento_extra

        # LÓGICA DE CONFORTO 
        gastos_essenciais = pessoa.salario * 0.9
        sobra = renda_total_recebida - gastos_essenciais
        
        pessoa.patrimonio += sobra
        pessoa.conforto = max(0, sobra / 1000)

    total_meses_simulados += 1
    valor_mes_simulados.set(str(total_meses_simulados))
    
    callback_atualizar_graficos(lista_de_pessoas_simulacao)

    return total_meses_simulados

def iniciar_simulacao(total_meses_simulados, meses_entry, valor_mes_simulados, callback_atualizar_graficos):
    try:
        meses = int(meses_entry.get())
        if meses <= 0:
            messagebox.showerror("Erro", "O número de meses deve ser maior que zero!")
            return total_meses_simulados
        
        for _ in range(meses):
            total_meses_simulados = simular_1_mes(total_meses_simulados, valor_mes_simulados, callback_atualizar_graficos)
        
        messagebox.showinfo("Simulação", f"Simulação de {meses} meses concluída!")
        return total_meses_simulados
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de meses!")
        return total_meses_simulados

def resetar_simulacao(meses_entry, valor_mes_simulados, pessoas_dados_iniciais, callback_atualizar_graficos):
    meses_entry.delete(0, tk.END)
    meses_entry.insert(0, "1")
    
    valor_mes_simulados.set("0")

    pessoas_resetadas = inicializar_objetos_pessoas(pessoas_dados_iniciais)
    callback_atualizar_graficos(pessoas_resetadas) 
    
    messagebox.showinfo("Reset", "Simulação resetada!")
    return 0




