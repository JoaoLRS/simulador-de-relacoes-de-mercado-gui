import tkinter as tk
from tkinter import messagebox, ttk

def iniciar_simulacao(total_meses_simulados, meses_entry, valor_mes_simulados):
    try:
        meses = int(meses_entry.get())
        if meses <= 0:
            messagebox.showerror("Erro", "O número de meses deve ser maior que zero!")
            return
        
        messagebox.showinfo("Simulação", f"Simulação iniciada para {meses} meses!")
        
        total_meses_simulados += meses
        valor_mes_simulados.set(str(total_meses_simulados))
        return total_meses_simulados
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de meses!")

def simular_1_mes(total_meses_simulados, valor_mes_simulados):
    # Simula especificamente 1 mês
    messagebox.showinfo("Simulação", "Simulação de 1 mês iniciada!")
    
    total_meses_simulados += 1
    valor_mes_simulados.set(str(total_meses_simulados))
    return total_meses_simulados

def resetar_simulacao(meses_entry, valor_mes_simulados):
    meses_entry.delete(0, tk.END)
    meses_entry.insert(0, "1")
    
    # Reseta o contador de meses simulados
    valor_mes_simulados.set("0")
    messagebox.showinfo("Reset", "Simulação resetada!")
    return 0




