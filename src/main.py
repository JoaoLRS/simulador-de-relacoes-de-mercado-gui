import tkinter as tk
from tkinter import messagebox, ttk
from funcoes_importantes import *


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




# Label e Entry para o número de meses para simular
meses_simular_label = tk.Label(main_frame, 
                                text="Meses para simular:",
                                font=("Arial", 16),
                                fg="black")
meses_simular_label.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))
meses_entry = tk.Entry(main_frame, 
                                font=("Arial", 16), 
                                width=5)


meses_entry.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))
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

simular_button = tk.Button(main_frame, 
                          text="Simular",
                          font=("Arial", 16),
                          command=iniciar_simulacao)
simular_button.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))


#Simular 1 mês 
simular_1_mes_button = tk.Button(main_frame, 
                                 text="Simular 1 mês",  
                                    font=("Arial", 16),
                                    command=simular_1_mes)
simular_1_mes_button.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))


#Resetar

reset_button = tk.Button(main_frame,
                        text="Resetar",
                        font=("Arial", 16),
                        command=resetar_simulacao)
reset_button.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))



#Monstrando meses simulados
meses_simulados_label = tk.Label(main_frame, 
                                text="Meses Simulados:",
                                font=("Arial", 16),
                                fg="black")
meses_simulados_label.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))
valor_mes_simulados = tk.StringVar()
valor_mes_simulados.set("0")
meses_simulados_value = tk.Label(main_frame, 
                                textvariable=valor_mes_simulados,
                                font=("Arial", 16),
                                fg="black")
meses_simulados_value.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))




# Posivel codigo para as abas 
# # Notebook para as abas
# notebook = ttk.Notebook(main_frame)
# notebook.pack(fill=tk.BOTH, expand=True)
       
# # Aba das categorias
# categoria_frame = tk.Frame(notebook)
# notebook.add(categoria_frame, text="Categorias")



root.mainloop()