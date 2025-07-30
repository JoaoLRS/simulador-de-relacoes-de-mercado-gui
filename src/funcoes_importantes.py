import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

lista_de_pessoas_simulacao = []
lista_de_empresas_simulacao = []

def inicializar_objetos_pessoas(pessoas_dados):
    from pessoa import Pessoa 
    global lista_de_pessoas_simulacao
    lista_de_pessoas_simulacao.clear()
    for p_dado in pessoas_dados:
        nome = p_dado["Nome"]
        patrimonio = float(p_dado["Patrimônio"].replace("R$ ", "").replace(".", "").replace(",", "."))
        salario = float(p_dado["Salário"].replace("R$ ", "").replace(".", "").replace(",", "."))
        pessoa_obj = Pessoa(nome, patrimonio, salario)
        # Inicializa rendimento_mensal 
        pessoa_obj.rendimento_mensal = pessoa_obj.salario + pessoa_obj.patrimonio * 0.005
        lista_de_pessoas_simulacao.append(pessoa_obj)
    return lista_de_pessoas_simulacao

def inicializar_objetos_empresas(empresas_objetos):
    global lista_de_empresas_simulacao
    lista_de_empresas_simulacao = empresas_objetos.copy()
    return lista_de_empresas_simulacao

def escolher_melhor_empresa(categoria, orcamento):
    melhor_empresa = None
    for empresa in lista_de_empresas_simulacao:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = empresa.get_preco()
            if preco <= orcamento:
                if melhor_empresa is None or empresa.qualidade > melhor_empresa.qualidade:
                    melhor_empresa = empresa
                elif empresa.qualidade == melhor_empresa.qualidade:
                    if preco < melhor_empresa.get_preco():
                        melhor_empresa = empresa
    return melhor_empresa

def simular_compras_pessoa(pessoa, categorias, percentuais):
    pessoa.conforto = 0.0  # Reset do conforto
    
    for i, categoria in enumerate(categorias):
        percentual = percentuais[categoria]
        orcamento_categoria = pessoa.rendimento_mensal * percentual
        
        # Escolhe a melhor empresa disponível
        empresa = escolher_melhor_empresa(categoria, orcamento_categoria)
        
        if empresa and empresa.vender_produto():
            # Deduz o valor gasto do patrimônio
            preco = empresa.get_preco()
            pessoa.patrimonio -= preco
            # Adiciona conforto baseado na qualidade
            pessoa.conforto += empresa.qualidade

def simular_mes_otimizado(pessoa):
    pessoa.rendimento_mensal = round(pessoa.rendimento_mensal * 1.0040646, 2)
    
    # LÓGICA DE CONFORTO e atualização de patrimônio
    gastos_essenciais = pessoa.salario * 0.9
    # calcula sobra com base na renda mensal atual
    sobra = pessoa.rendimento_mensal - gastos_essenciais
    # incrementa patrimônio conforme sobra
    pessoa.patrimonio += sobra
    
    # Simula compras nas empresas baseado nas categorias
    simular_compras_pessoa_completa(pessoa)

def carregar_categorias_gastos():
    BASE_DIR = os.path.dirname(__file__)
    path = os.path.join(BASE_DIR, 'dados', 'categorias.json')
    
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def simular_compras_pessoa_completa(pessoa):
    pessoa.conforto = 0.0  # Reset do conforto

    categorias_gastos = carregar_categorias_gastos()
    
    for categoria, percentual in categorias_gastos.items():
        orcamento_categoria = pessoa.rendimento_mensal * percentual
        
        # Escolhe a melhor empresa disponível
        empresa = escolher_melhor_empresa(categoria, orcamento_categoria)
        
        if empresa and empresa.vender_produto():
            # Deduz o valor gasto do patrimônio
            preco = empresa.get_preco()
            pessoa.patrimonio -= preco
            # Adiciona conforto baseado na qualidade
            pessoa.conforto += empresa.qualidade
    
    # Define conforto máximo de 40
    pessoa.conforto = min(pessoa.conforto, 40)

def simular_empresas_mes():
    for empresa in lista_de_empresas_simulacao:
        # Repõe estoque no início do mês
        empresa.repor_estoque()
        # Reset vendas do mês anterior
        empresa.vendas = 0

def simular_empresas_fim_mes():
    for empresa in lista_de_empresas_simulacao:
        # Ajusta estratégias baseado no desempenho
        empresa.ajustar_estrategia()

def simular_1_mes(total_meses_simulados, valor_mes_simulados, callback_atualizar_graficos, atualizar_interface=True):
    global lista_de_pessoas_simulacao

    # Simula um mês nas empresas primeiro 
    simular_empresas_mes()

    # Lógica de simulação para pessoas 
    for pessoa in lista_de_pessoas_simulacao:
        simular_mes_otimizado(pessoa)

    # Ajusta estratégias das empresas no final do mês
    simular_empresas_fim_mes()

    total_meses_simulados += 1
    valor_mes_simulados.set(str(total_meses_simulados))
    
    # Só atualiza a interface se solicitado
    if atualizar_interface:
        callback_atualizar_graficos(lista_de_pessoas_simulacao)

    return total_meses_simulados

def iniciar_simulacao(total_meses_simulados, meses_entry, valor_mes_simulados, callback_atualizar_graficos):
    try:
        meses = int(meses_entry.get())
        if meses <= 0:
            messagebox.showerror("Erro", "O número de meses deve ser maior que zero!")
            return total_meses_simulados
        
        if meses > 100:
            for _ in range(meses):
                simular_empresas_mes()  # Início do mês
                for pessoa in lista_de_pessoas_simulacao:
                    simular_mes_otimizado(pessoa)
                simular_empresas_fim_mes()  # Final do mês
                total_meses_simulados += 1
            

            valor_mes_simulados.set(str(total_meses_simulados))
            callback_atualizar_graficos(lista_de_pessoas_simulacao)
        else:
            for i in range(meses):
                atualizar_interface = (i == meses - 1) or (meses > 24 and i % 12 == 0)
                total_meses_simulados = simular_1_mes(total_meses_simulados, valor_mes_simulados, callback_atualizar_graficos, atualizar_interface)
        
        messagebox.showinfo("Simulação", f"Simulação de {meses} meses concluída com sucesso!")
        return total_meses_simulados
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de meses!")
        return total_meses_simulados

def resetar_simulacao(meses_entry, valor_mes_simulados, pessoas_dados_iniciais, callback_atualizar_graficos):
    global lista_de_empresas_simulacao
    meses_entry.delete(0, tk.END)
    meses_entry.insert(0, "1")
    
    valor_mes_simulados.set("0")

    # Reseta pessoas
    pessoas_resetadas = inicializar_objetos_pessoas(pessoas_dados_iniciais)
    
    # Reseta empresas 
    for empresa in lista_de_empresas_simulacao:
        empresa.vendas = 0
        empresa.lucro_total = 0.0
        empresa.margem = 0.05 
        empresa.oferta = 10    
        empresa.reposicao = 10
        empresa.meses_sem_venda = 0
    
    callback_atualizar_graficos(pessoas_resetadas) 
    
    messagebox.showinfo("Reset", "Simulação resetada!")
    return 0




